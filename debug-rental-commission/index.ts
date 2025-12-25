const { agreementNo, invoiceNo } = inputs;
const database = "COMMISSION_DB";

// Helper to execute and parse Query safely
async function query(sql) {
  try {
    const res = await db_prod_execute_query({ query: sql });
    if (res.success && !res.data.isError && res.data.content && res.data.content.length > 0) {
       const parsed = JSON.parse(res.data.content[0].text);
       return parsed.recordset || [];
    }
    console.log("Query Failed or Empty:", res);
    return [];
  } catch (e) {
    console.log("Execution Error:", e.message);
    return [];
  }
}

console.log(`🔍 Starting Rental Commission Investigation for Agreement: ${agreementNo}`);

// 1. Get Agreement Details
const agreementRes = await query(`USE ${database}; SELECT * FROM RENTAL_AGREEMENT WHERE agreement = '${agreementNo}'`);

if (!agreementRes.length) {
  console.log("❌ Agreement not found or query failed.");
} else {
    const agreement = agreementRes[0];
    console.log(`\n📋 Agreement Details:\n- Customer: ${agreement['Customer Name']}\n- Status: ${agreement.status}\n- Start: ${agreement.custom_etd}\n- End: ${agreement.enddate}\n- Salesman: ${agreement.custom_salesmancode}\n- Bill Cycle: ${agreement.billcycle}`);
}

// 2. Get Settlements (Source of "Callbacks")
const settlements = await query(`USE ${database}; SELECT * FROM RENTAL_SETTLEMENT WHERE billing_agreementid = '${agreementNo}' ORDER BY LASTSETTLEDATE DESC`);

// 3. Get Commissions
const commissions = await query(`USE ${database}; SELECT * FROM RENTAL_COMMISSION WHERE RA = '${agreementNo}'`);

// 4. Get Payments
let payments = [];
if (settlements.length > 0) {
    const invoices = settlements.map(s => `'${s.INVOICEID}'`).join(',');
    if (invoices) {
        payments = await query(`USE ${database}; SELECT * FROM RENTAL_PAYMENT WHERE INVOICE IN (${invoices})`);
    }
}

// Analyze each settlement
console.log(`\n🔎 Analyzing Settlements & Commissions (${settlements.length} found):`);

// Safe table function
function printTable(data) {
    if (console.table) {
        console.table(data);
    } else {
        console.log(JSON.stringify(data, null, 2));
    }
}

const analysis = settlements.map(settlement => {
  const inv = settlement.INVOICEID;
  const voucher = settlement.LASTSETTLEVOUCHER;
  const amount = settlement.SETTLEAMOUNTCUR;
  const dateStr = settlement.LASTSETTLEDATE;
  
  // Find matching commission
  const comm = commissions.find(c => c.INV === inv);
  
  let status = "✅ OK";
  let reason = "";

  if (comm) {
    status = "✅ Processed";
  } else {
    status = "❌ MISSING";
    
    // logic based on user feedback
    if (voucher && voucher.startsWith('CNV')) {
      reason = "⚠️ Reason: Credit Note/Offset (CNV). Skipped by script.";
    } else if (voucher && voucher.startsWith('RV')) {
       // Check if it's a deposit
       if (settlement.billing_schedule === 'DEPOSIT' || (settlement.BILLINGCODE && settlement.BILLINGCODE.includes('DPS'))) {
           reason = "ℹ️ Reason: Deposit (Excl.)";
           status = "ℹ️ Deposit";
       } else {
           reason = "⚠️ Reason: Unknown. Valid RV. Check Script/Cycle 1.";
       }
    } else if (!voucher) {
      reason = "⚠️ Reason: Outstanding (No Voucher)";
    }
  }

  // Check for Bill Cycle 1 issue
  const isCycle1 = settlement.billing_cycle === 1 || (settlement.BILLINGCODE && settlement.BILLINGCODE.includes('TERM_1'));
  if (isCycle1 && status.includes('MISSING')) {
      reason += " (Possibility: Cycle 1 Cancelled)";
  }

  return {
    invoice: inv,
    date: dateStr ? (dateStr + '').split('T')[0] : 'N/A', // Safer string coercion
    amount: amount,
    voucher: voucher || 'NONE',
    status: status,
    reason: reason
  };
});

if (analysis.length > 0) {
    printTable(analysis);
} else {
    console.log("No settlements found.");
}

// Summarize
const missing = analysis.filter(a => a.status.includes('MISSING'));
if (missing.length > 0) {
    console.log(`\n⚠️ Found ${missing.length} invoices with MISSING commission.`);
    missing.forEach(m => {
        console.log(`- Invoice ${m.invoice} ($${m.amount}): ${m.reason}`);
    });
    console.log("\n💡 Recommendation: CNV = Not Eligible (Offset). RV + Missing = Check script logs or manual processing.");
} else {
    console.log("\n✅ All eligible settlements appear to have commissions.");
}

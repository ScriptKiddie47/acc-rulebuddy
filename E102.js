function evaluateRuleE102(requestJson) {
  const data = requestJson.data;
  const hasHighPriorYrIssaCnt = data.coverageParts.some(
    part => part.priorYrIssaCnt > 300
  );

  if (data.issuingBusinessUnitCdGvng === "10" && hasHighPriorYrIssaCnt) {
    return {
      ruleTriggered: true,
      ruleId: "E102",
      reasonCd: "Prior year issuance count exceeds threshold for BU 10"
    };
  }

  return {
    ruleTriggered: false
  };
}

// Sample input JSON
const requestJson = {
  "data": {
    "uniqueID": "1",
    "issuingBusinessUnitCdGvng": "10",
    "coverageParts": [
      {
        "priorYrIssaCnt": 350.0,
        "covPartCd": "AU",
        "govratingStateCd": "PA",
        "coverages": [],
        "linesOfInsurance": [],
        "covPartStates": [],
        "Vehicles": []
      }
    ],
    "namedInsured": {},
    "locations": [],
    "effectiveDt": "2025-07-14",
    "formCd": "BA",
    "expirationDt": "2025-07-14",
    "transaction": {},
    "businessClassCdGvng": "r55"
  }
};

console.log(evaluateRuleE102(requestJson));

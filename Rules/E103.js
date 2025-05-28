function evaluateE103Rule(requestJson) {
   // request AddSourceCoverageCdRequest.json
    const data = requestJson.data;

    const programCdGvngLeg = data.programCdGvngLeg;
    const effectiveDt = new Date(data.effectiveDt);
    const ruleEffectiveDate = new Date("2025-07-14");

    // Check global-level conditions first
    if (programCdGvngLeg === "P54" || effectiveDt < ruleEffectiveDate) {
        return { ruleTriggered: false };
    }

    const coverageParts = data.coverageParts || [];

    for (const coveragePart of coverageParts) {
        const priorYrIssaCnt = coveragePart.priorYrIssaCnt || 0;

        if (priorYrIssaCnt >= 4000) {
            const vehicles = coveragePart.Vehicles || [];

            for (const vehicle of vehicles) {
                const coverages = vehicle.coverages || [];

                for (const coverage of coverages) {
                    if (coverage.classCode === "01121") {
                        return {
                            ruleTriggered: true,
                            ruleNumber: "E103",
                            reasonCode: "Rule E103 triggered due to: programCdGvngLeg ≠ 'P54', priorYrIssaCnt ≥ 4000, classCode = '01121', effectiveDt ≥ 2025-07-14"
                        };
                    }
                }
            }
        }
    }

    return { ruleTriggered: false };
}

const requestJson = {
  "data": {
    "uniqueID": "1",
    "drChgNwdSbUblHierarchyNbr": 0,
    "action": "add",
    "type": "Policy",
    "programCdGvngLeg": "P55",
    "reportingOfficeCdLeg": "084",
    "policyNbr": "00A12675A",
    "issuingBusinessUnitCdGvng": "14",
    "brandCd": "BAP",
    "coverageParts": [
      {
        "uniqueID": "2",
        "drChgNwdSbUblHierarchyNbr": 0,
        "dataTxt": "",
        "action": "add",
        "type": "AutoCoveragePart",
        "industrySegmentTypeCdGvng": "18",
        "programCdGvng": "P55",
        "businessClassCdGvng": "P55",
        "priorYrIssaCnt": 60000,
        "covPartCd": "AU",
        "govratingStateCd": "PA",
        "coverages": [],
        "linesOfInsurance": [],
        "covPartStates": [
          {
            "type": "Coverage",
            "sourceCoverageCd": "EMPHIRE"
          }
        ],
        "Vehicles": [
          {
            "uniqueID": "9",
            "action": "add",
            "type": "Vehicle",
            "coverages": [
              {
                "uarSequenceNbr": 1,
                "classCode": "01121",
                "stateCode": "PA",
                "bureauVehicleClassIdCd": "LTRK",
                "vehicleGroupTypeCd": "TTT",
                "makeCd": "FORD",
                "vehicleIdentificationNbr": "1FTNE24L09DA25896",
                "makeNm": "FORD",
                "commercialVehicleBusinessUseCd": "S",
                "commercialVehicleBusinessSubUseCd": "01",
                "vehicleClassification": {
                  "drvChgWorkSubHierarchyNbr": 0,
                  "type": "VehicleClassification",
                  "selfPropelledVehicleInd": false,
                  "pptLtrkVehicleUseTypeCd": "B"
                },
                "garagingStatePostalCd": "15211-4203"
              }
            ]
          }
        ],
        "autoCovPartStates": [],
        "coverageSymbolsGroups": []
      }
    ],
    "selfPropelledVehicleCnt": 1,
    "fleetInd": false,
    "trailerCnt": 0,
    "licensePlateCnt": 0,
    "accountMultilineInd": true,
    "drvAutoGaragingStates": [],
    "totalDriverCnt": 1,
    "namedInsured": {},
    "locations": [],
    "effectiveDt": "2025-07-14",
    "formCd": "BA",
    "expirationDt": "2025-07-14",
    "transaction": {},
    "businessClassCdGvng": "P55",
    "policyID": 21567843
  }
};
console.log(evaluateE103Rule(requestJson));

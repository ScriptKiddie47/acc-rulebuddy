function validateE101(requestJson) {
    const errors = [];
    // Request 9881923218.json
    const data = requestJson.data;
    if (!data?.coverageParts) return errors;

    data.coverageParts.forEach((coveragePart, partIndex) => {
        if (!coveragePart.Vehicles) return;

        coveragePart.Vehicles.forEach((vehicle, vehicleIndex) => {
            if (!vehicle.coverages) return;

            vehicle.coverages.forEach((coverage, coverageIndex) => {
                const { stateCode, bureauVehicleClassIdCd, vehicleGroupTypeCd } = coverage;

                if (
                    stateCode !== "CA" &&
                    bureauVehicleClassIdCd === "LTRK" &&
                    vehicleGroupTypeCd === "TTT"
                ) {
                    errors.push({
                        ruleId: "E101",
                        message: "Invalid vehicle group type for bureau vehicle class KAJS in non-CA state.",
                        path: `coverageParts[${partIndex}].Vehicles[${vehicleIndex}].coverages[${coverageIndex}]`
                    });
                }
            });
        });
    });

    return errors;
}

// Sample input JSON
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
        "priorYrIssaCnt": 0,
        "covPartCd": "AU",
        "govratingStateCd": "PA",
        "coverages": [],
        "linesOfInsurance": [],
        "covPartStates": [],
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
                "vehicleIdentificationNbr": "1FRK24L09DA25896",
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
    "businessClassCdGvng": "P55"
  }
};

console.log(validateE101(requestJson));

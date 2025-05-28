function evaluateE104Rule(request) {
     // request AddVehicles_Request1.json
    const data = request.data;
    const effectiveDt = new Date(data.effectiveDt);
    const ruleEffectiveDate = new Date("2025-07-14");

    // Check effective date condition
    if (effectiveDt < ruleEffectiveDate) {
        return { ruleTriggered: false };
    }

    const coverageParts = data.coverageParts || [];

    for (const coveragePart of coverageParts) {
        const vehicles = coveragePart.Vehicles || [];

        for (const vehicle of vehicles) {
            const coverages = vehicle.coverages || [];

            for (const coverage of coverages) {
                const classification = coverage.vehicleClassification;

                if (
                    classification?.type === "VehicleClassification" &&
                    classification?.selfPropelledVehicleInd === false &&
                    coverage.uarSequenceNbr >= 1
                ) {
                    return {
                        ruleTriggered: true,
                        ruleNumber: "E104",
                        reasonCode: "Rule E104 triggered due to: vehicleClassification.type = 'VehicleClassification', selfPropelledVehicleInd = false, uarSequenceNbr ≥ 1, and effectiveDt ≥ 2025-07-14"
                    };
                }
            }
        }
    }

    return { ruleTriggered: false };
}
const requestJson = {
  data: {
    uniqueID: "1",
    drChgNwdSbUblHierarchyNbr: 0,
    action: "add",
    type: "Policy",
    programCdGvngLeg: "P55",
    reportingOfficeCdLeg: "084",
    policyNbr: "00A12675A",
    issuingBusinessUnitCdGvng: "14",
    brandCd: "BAP",
    coverageParts: [
      {
        uniqueID: "2",
        drChgNwdSbUblHierarchyNbr: 0,
        dataTxt: "",
        action: "add",
        type: "AutoCoveragePart",
        industrySegmentTypeCdGvng: "18",
        programCdGvng: "P55",
        businessClassCdGvng: "P55",
        priorYrIssaCnt: 0,
        covPartCd: "AU",
        govratingStateCd: "PA",
        coverages: [],
        linesOfInsurance: [],
        covPartStates: [
          {
            type: "Coverage",
            sourceCoverageCd: "EMPHIRE"
          }
        ],
        Vehicles: [
          {
            uniqueID: "9",
            action: "add",
            type: "Vehicle",
            coverages: [
              {
                uarSequenceNbr: 1,
                classCode: "01121",
                stateCode: "PA",
                bureauVehicleClassIdCd: "LTRK",
                vehicleGroupTypeCd: "TTT",
                makeCd: "FORD",
                vehicleIdentificationNbr: "1FTNE24L09DA25896",
                makeNm: "FORD",
                commercialVehicleBusinessUseCd: "S",
                commercialVehicleBusinessSubUseCd: "01",
                vehicleClassification: {
                  drvChgWorkSubHierarchyNbr: 0,
                  type: "VehicleClassification",
                  selfPropelledVehicleInd: false,
                  pptLtrkVehicleUseTypeCd: "B"
                },
                garagingStatePostalCd: "15211-4203"
              }
            ]
          }
        ],
        autoCovPartStates: [],
        coverageSymbolsGroups: []
      }
    ],
    selfPropelledVehicleCnt: 1,
    fleetInd: false,
    trailerCnt: 0,
    licensePlateCnt: 0,
    accountMultilineInd: true,
    drvAutoGaragingStates: [],
    totalDriverCnt: 1,
    namedInsured: {},
    locations: [],
    effectiveDt: "2025-07-14",
    formCd: "BA",
    expirationDt: "2025-07-14",
    transaction: {},
    businessClassCdGvng: "P55",
    policyID: 21567843
  }
};
console.log(evaluateE104Rule(requestJson));

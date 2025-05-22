function evaluateE104Rule(request) {
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

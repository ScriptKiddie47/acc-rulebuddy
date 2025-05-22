function evaluateE103Rule(request) {
    const data = request.data;

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

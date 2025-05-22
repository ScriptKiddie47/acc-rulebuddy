function validateE101(data) {
    const errors = [];
// request AddVehicles_Request1.json
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
                    vehicleGroupTypeCd === "TIL"
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

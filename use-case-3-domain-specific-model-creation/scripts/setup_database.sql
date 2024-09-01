-- Connect to the database
\c eln_experiments

-- Create the experiments table
CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    experiment_name VARCHAR(255) NOT NULL,
    researcher VARCHAR(100) NOT NULL,
    date_conducted DATE NOT NULL,
    equipment_used TEXT[],
    reagents JSONB,
    temperature DECIMAL(5,2),
    pressure DECIMAL(8,2),
    duration INTERVAL,
    notes TEXT,
    extracted_method JSONB
);

INSERT INTO experiments (experiment_name,researcher,date_conducted,equipment_used,reagents,temperature,pressure,duration,notes,extracted_method) VALUES
	 ('Synthesis of Gold Nanoparticles','Dr. Jane Smith','2023-08-15','{"Hot plate","Magnetic stirrer","UV-Vis spectrometer"}','{"Trisodium citrate": "1% w/v", "Gold(III) chloride trihydrate": "0.01 M"}',95.50,101.33,'02:00:00'::interval,'Experiment: Synthesis of Gold Nanoparticles
    Equipment: Hot plate, magnetic stirrer, glassware, UV-Vis spectrometer
    Reagents: Gold(III) chloride trihydrate (HAuCl4·3H2O), trisodium citrate
    Procedure:
    1. Prepared 20 mL of 1 mM HAuCl4 solution in a 50 mL beaker.
    2. Heated the solution to boiling while stirring.
    3. Rapidly added 2 mL of a 1% solution of trisodium citrate dihydrate.
    4. Continued heating and stirring until the solution turned deep red (about 10 minutes).
    5. Removed from heat and allowed to cool to room temperature.
    6. Performed UV-Vis spectroscopy to confirm nanoparticle formation.
    Observations: Solution changed from pale yellow to colorless, then to dark purple, and finally to deep red.','{"results": "The solution underwent a color change, indicating the successful synthesis of Gold Nanoparticles.", "objective": "The main goal of the experiment was to synthesize Gold Nanoparticles using a method that involved heating a solution of Gold(III) chloride trihydrate and trisodium citrate dihydrate.", "procedure": ["1. Prepared 20 mL of 1 mM Gold(III) chloride trihydrate solution in a 50 mL beaker.", "2. Heated the solution to boiling while stirring.", "3. Rapidly added 2 mL of a 1% solution of trisodium citrate dihydrate.", "4. Continued heating and stirring until the solution turned deep red (about 10 minutes).", "5. Removed from heat and allowed to cool to room temperature.", "6. Performed UV-Vis spectroscopy to confirm nanoparticle formation."], "observations": "Solution changed from pale yellow to colorless, then to dark purple, and finally to deep red.", "equipment_setup": "Hot plate, magnetic stirrer, glassware, UV-Vis spectrometer were set up and used to prepare the solution, heat it, stir it, and confirm nanoparticle formation respectively."}'),
	 ('Polymerase Chain Reaction','Dr. John Doe','2023-09-01','{"Thermal cycler",Microcentrifuge,"Gel electrophoresis apparatus"}','{"MgCl2": "25 mM", "dNTPs": "10 mM each", "Primers": "10 µM each", "Taq polymerase": "5 U/µL"}',72.00,101.33,'03:00:00'::interval,'Experiment: Polymerase Chain Reaction (PCR) for Gene Amplification
    Equipment: Thermal cycler, microcentrifuge, gel electrophoresis apparatus
    Reagents: Taq polymerase, dNTPs, MgCl2, forward and reverse primers, template DNA
    Procedure:
    1. Prepared PCR master mix containing buffer, dNTPs, MgCl2, and Taq polymerase.
    2. Added primers and template DNA to individual PCR tubes.
    3. Placed tubes in thermal cycler and ran the following program:
       a. Initial denaturation: 95°C for 3 minutes
       b. 30 cycles of:
          - Denaturation: 95°C for 30 seconds
          - Annealing: 55°C for 30 seconds
          - Extension: 72°C for 1 minute
       c. Final extension: 72°C for 5 minutes
    4. Ran PCR products on a 1% agarose gel to confirm amplification.
    Observations: Clear bands observed on the gel at the expected size of 500 bp.','{"results": "The results showed successful amplification of the targeted DNA region.", "objective": "The main goal of the experiment was to amplify a specific region of DNA using Polymerase Chain Reaction (PCR) method.", "procedure": {"step1": "Prepared PCR master mix containing buffer, dNTPs, MgCl2, and Taq polymerase.", "step2": "Added primers and template DNA to individual PCR tubes.", "step3": {"substep1": "Placed tubes in thermal cycler", "substeps_cycles": [{"annealing": "55°C for 30 seconds", "extension": "72°C for 1 minute", "denaturation": "95°C for 3 minutes"}, {"loop_num": "30", "annealing": "55°C for 30 seconds", "extension": "72°C for 1 minute", "denaturation": "95°C for 30 seconds"}, {"final_extension": "72°C for 5 minutes"}]}}, "observations": "Clear bands observed on the gel at the expected size of 500 bp.", "equipment_setup": "The equipment used for this experiment included a thermal cycler, microcentrifuge, and gel electrophoresis apparatus. The temperature of the thermal cycler was set to 72.00°C, the pressure was at 101.33 kPa, and the duration was 3:00:00."}'),
	 ('Protein Crystallization','Dr. Emily Chen','2023-09-10','{"Crystallization robot","Light microscope",Incubator}','{"PEG 3350": "20% w/v", "HEPES buffer": "0.1 M, pH 7.5", "Protein sample": "10 mg/mL", "Ammonium sulfate": "0.2 M"}',20.00,101.33,'7 days'::interval,'Experiment: Protein Crystallization using Hanging Drop Vapor Diffusion
    Equipment: Crystallization robot, light microscope, incubator
    Reagents: Purified protein sample, PEG 3350, ammonium sulfate, HEPES buffer
    Procedure:
    1. Prepared crystallization screens varying PEG 3350 concentration (10-30%) and pH (6.5-8.5).
    2. Used crystallization robot to set up 96-well hanging drop vapor diffusion plates.
    3. Mixed 1 µL of protein sample with 1 µL of reservoir solution in each drop.
    4. Sealed plates and incubated at 20°C.
    5. Monitored crystal growth daily using a light microscope.
    Observations: Small crystal nuclei observed after 3 days in conditions with 20% PEG 3350 and pH 7.5. Crystals continued to grow over the next 4 days.','{"results": "The experiment resulted in the successful growth of protein crystals, with small crystal nuclei observed after 3 days in conditions with 20% PEG 3350 and pH 7.5.", "objective": "The main goal of the experiment was to observe and grow protein crystals using the Hanging Drop Vapor Diffusion method.", "procedure": ["Prepared crystallization screens varying PEG 3350 concentration (10-30%) and pH (6.5-8.5).", "Used the crystallization robot to set up 96-well hanging drop vapor diffusion plates.", "Mixed 1 µL of protein sample with 1 µL of reservoir solution in each drop.", "Sealed the plates and incubated them at 20°C.", "Monitored crystal growth daily using a light microscope."], "observations": "Small crystal nuclei were observed after 3 days in conditions with 20% PEG 3350 and pH 7.5. Crystals continued to grow over the next 4 days.", "equipment_setup": "The experiment was conducted using a Crystallization robot, a Light microscope, and an Incubator. The Crystallization robot was utilized to set up 96-well hanging drop vapor diffusion plates. These plates were sealed and incubated at 20°C."}');

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE eln_experiments TO eln_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO eln_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO eln_user;
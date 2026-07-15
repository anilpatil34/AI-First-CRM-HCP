-- =============================================================
-- AI-First Healthcare CRM — Seed Data
-- Populates the database with sample records for development
-- =============================================================

-- =============================================================
-- HCP Profiles (10 sample doctors)
-- =============================================================
INSERT INTO hcp_profiles (id, name, hospital, specialization, phone, email, preferred_contact, notes) VALUES
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567801', 'Dr. Priya Sharma', 'Apollo Hospital, Mumbai', 'Cardiology', '+91-9876543210', 'priya.sharma@apollo.com', 'email', 'Key opinion leader in interventional cardiology. Prefers morning meetings.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567802', 'Dr. Rajesh Patel', 'Fortis Hospital, Delhi', 'Endocrinology', '+91-9876543211', 'rajesh.patel@fortis.com', 'phone', 'Interested in new diabetes management therapies. Very research-oriented.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567803', 'Dr. Ananya Reddy', 'KIMS Hospital, Hyderabad', 'Oncology', '+91-9876543212', 'ananya.reddy@kims.com', 'in-person', 'Heads the oncology department. Focused on immunotherapy treatments.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567804', 'Dr. Vikram Singh', 'Max Hospital, Bangalore', 'Neurology', '+91-9876543213', 'vikram.singh@maxhospital.com', 'video-call', 'Specialist in epilepsy and movement disorders. Active in clinical trials.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567805', 'Dr. Meera Joshi', 'Lilavati Hospital, Mumbai', 'Pulmonology', '+91-9876543214', 'meera.joshi@lilavati.com', 'email', 'Interested in COPD and asthma treatments. Publishes regularly.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567806', 'Dr. Arjun Nair', 'Amrita Hospital, Kochi', 'Orthopedics', '+91-9876543215', 'arjun.nair@amrita.com', 'phone', 'Sports medicine specialist. Consults for IPL teams.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567807', 'Dr. Sneha Kulkarni', 'Ruby Hall Clinic, Pune', 'Dermatology', '+91-9876543216', 'sneha.kulkarni@rubyhall.com', 'in-person', 'Focuses on biologics for psoriasis treatment.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567808', 'Dr. Amir Khan', 'Medanta Hospital, Gurugram', 'Gastroenterology', '+91-9876543217', 'amir.khan@medanta.com', 'email', 'Expert in IBD management. Interested in new biologic therapies.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567809', 'Dr. Kavita Deshmukh', 'Kokilaben Hospital, Mumbai', 'Rheumatology', '+91-9876543218', 'kavita.deshmukh@kokilaben.com', 'video-call', 'Researches autoimmune conditions. Open to new JAK inhibitors.'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567810', 'Dr. Sanjay Gupta', 'AIIMS, Delhi', 'General Medicine', '+91-9876543219', 'sanjay.gupta@aiims.com', 'phone', 'Senior professor. Influential in formulary decisions.');

-- =============================================================
-- Materials (10 sample marketing/educational materials)
-- =============================================================
INSERT INTO materials (id, name, type, description) VALUES
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567801', 'CardioGuard Product Brochure', 'brochure', 'Comprehensive brochure covering CardioGuard mechanism of action, dosing, and patient outcomes.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567802', 'Phase III STELLAR Trial Results', 'clinical-study', 'Published results from the STELLAR cardiovascular outcomes trial (N=12,000).'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567803', 'GlucoBalance Product Sheet', 'product-sheet', 'One-page summary of GlucoBalance for Type 2 Diabetes with dosing chart.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567804', 'ImmunoShield Mechanism of Action', 'presentation', '25-slide deck explaining the immunotherapy mechanism of ImmunoShield.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567805', 'NeuroCalm Safety Profile Whitepaper', 'whitepaper', 'Detailed safety and tolerability data for NeuroCalm from 3-year follow-up study.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567806', 'BreatheEasy Clinical Evidence Summary', 'clinical-study', 'Summary of 5 clinical trials supporting BreatheEasy for COPD management.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567807', 'FlexiJoint Patient Outcomes Video', 'video', 'Patient testimonial and outcomes video for FlexiJoint joint supplement.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567808', 'DermaClear Prescribing Guide', 'brochure', 'Prescribing information and quick-reference guide for DermaClear biologic.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567809', 'GutHealth Comparative Study', 'clinical-study', 'Head-to-head comparative study of GutHealth vs. standard of care in IBD.'),
    ('b1b2c3d4-e5f6-7890-abcd-ef1234567810', 'Company Portfolio Overview 2026', 'presentation', 'Full product portfolio presentation for the current fiscal year.');

-- =============================================================
-- Samples (10 sample pharmaceutical products)
-- =============================================================
INSERT INTO samples (id, name, product, quantity) VALUES
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567801', 'CardioGuard 10mg Starter Pack', 'CardioGuard', 100),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567802', 'CardioGuard 20mg Tablets', 'CardioGuard', 75),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567803', 'GlucoBalance 500mg Tabs', 'GlucoBalance', 120),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567804', 'GlucoBalance Pen Injector', 'GlucoBalance', 30),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567805', 'ImmunoShield 100mg Vial', 'ImmunoShield', 25),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567806', 'NeuroCalm 25mg Capsules', 'NeuroCalm', 80),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567807', 'BreatheEasy Inhaler', 'BreatheEasy', 50),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567808', 'FlexiJoint Gel 50g', 'FlexiJoint', 60),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567809', 'DermaClear Cream 30g', 'DermaClear', 45),
    ('c1b2c3d4-e5f6-7890-abcd-ef1234567810', 'GutHealth 250mg Capsules', 'GutHealth', 90);

-- =============================================================
-- Interactions (5 sample interactions)
-- =============================================================
INSERT INTO hcp_interactions (id, hcp_id, interaction_type, date, time, attendees, topics_discussed, sentiment, outcomes, follow_up_actions, summary, ai_generated) VALUES
    (
        'd1b2c3d4-e5f6-7890-abcd-ef1234567801',
        'a1b2c3d4-e5f6-7890-abcd-ef1234567801',
        'in-person',
        '2026-07-01',
        '10:30:00',
        ARRAY['Dr. Priya Sharma', 'Sales Rep: Anil Patil', 'MSL: Rohit Mehta'],
        ARRAY['CardioGuard efficacy data', 'STELLAR trial outcomes', 'Patient selection criteria'],
        'positive',
        'Dr. Sharma agreed to trial CardioGuard for 5 new patients. Requested additional data on elderly subgroup analysis.',
        ARRAY['Send elderly subgroup analysis by July 5', 'Schedule follow-up visit in 2 weeks', 'Arrange KOL speaker event at Apollo'],
        'Productive meeting with Dr. Priya Sharma at Apollo Hospital. Discussed STELLAR trial results for CardioGuard with focus on cardiovascular outcomes. Dr. Sharma was impressed with the 23% risk reduction data and agreed to prescribe for 5 new patients. She requested additional subgroup analysis data for patients above 65 years of age. Follow-up scheduled for mid-July.',
        true
    ),
    (
        'd1b2c3d4-e5f6-7890-abcd-ef1234567802',
        'a1b2c3d4-e5f6-7890-abcd-ef1234567802',
        'phone',
        '2026-07-02',
        '14:00:00',
        ARRAY['Dr. Rajesh Patel', 'Sales Rep: Anil Patil'],
        ARRAY['GlucoBalance new formulation', 'HbA1c reduction data', 'Insurance coverage'],
        'neutral',
        'Dr. Patel wants to compare GlucoBalance with competitor. Will review materials and respond next week.',
        ARRAY['Email comparative study PDF', 'Check insurance formulary status', 'Follow up next Wednesday'],
        'Phone call with Dr. Rajesh Patel regarding the new GlucoBalance formulation. Discussed HbA1c reduction data and compared favorably to existing options. Dr. Patel is cautious and wants to see head-to-head data before switching patients. Insurance coverage question raised — need to verify formulary status.',
        true
    ),
    (
        'd1b2c3d4-e5f6-7890-abcd-ef1234567803',
        'a1b2c3d4-e5f6-7890-abcd-ef1234567803',
        'in-person',
        '2026-07-03',
        '11:00:00',
        ARRAY['Dr. Ananya Reddy', 'Sales Rep: Anil Patil', 'Medical Director: Dr. Suman Rao'],
        ARRAY['ImmunoShield clinical data', 'Combination therapy protocols', 'Patient assistance programs'],
        'positive',
        'Dr. Reddy enthusiastic about ImmunoShield for second-line treatment. Wants to enroll patients in the patient assistance program.',
        ARRAY['Send patient assistance program enrollment forms', 'Arrange tumor board presentation', 'Provide combination therapy dosing guidelines'],
        'Met Dr. Ananya Reddy at KIMS Hospital with Medical Director Dr. Suman Rao. Presented ImmunoShield immunotherapy data for second-line treatment of advanced cases. Dr. Reddy showed strong interest, particularly in combination therapy with existing protocols. She requested patient assistance program details for uninsured patients. Agreed to present at the next tumor board meeting.',
        true
    ),
    (
        'd1b2c3d4-e5f6-7890-abcd-ef1234567804',
        'a1b2c3d4-e5f6-7890-abcd-ef1234567805',
        'video-call',
        '2026-07-05',
        '16:00:00',
        ARRAY['Dr. Meera Joshi', 'Sales Rep: Anil Patil'],
        ARRAY['BreatheEasy device training', 'COPD exacerbation prevention', 'Real-world evidence'],
        'positive',
        'Dr. Joshi impressed with BreatheEasy device design. Will recommend to patients struggling with existing inhalers.',
        ARRAY['Ship 10 demo devices to clinic', 'Send real-world evidence publication', 'Schedule nurse training session'],
        'Video call with Dr. Meera Joshi to demonstrate the BreatheEasy inhaler device. Covered proper technique, dose counter features, and patient-friendly design. Discussed real-world evidence showing 40% reduction in COPD exacerbations. Dr. Joshi found the device intuitive and will recommend it to patients having difficulty with current inhalers.',
        true
    ),
    (
        'd1b2c3d4-e5f6-7890-abcd-ef1234567805',
        'a1b2c3d4-e5f6-7890-abcd-ef1234567808',
        'email',
        '2026-07-07',
        NULL,
        ARRAY['Dr. Amir Khan', 'Sales Rep: Anil Patil'],
        ARRAY['GutHealth study results', 'IBD treatment guidelines', 'Upcoming symposium'],
        'neutral',
        'Dr. Khan reviewed the comparative study. Wants to discuss findings at the upcoming GI symposium.',
        ARRAY['Register Dr. Khan for GI symposium', 'Prepare symposium presentation slides', 'Send updated treatment algorithm'],
        'Email exchange with Dr. Amir Khan regarding the GutHealth comparative study results in IBD. Dr. Khan found the data interesting but wants more context on long-term remission rates. He will be attending the upcoming GI symposium and suggested discussing further there. Agreed to register him as a speaker at the event.',
        true
    );

-- =============================================================
-- Interaction-Materials links
-- =============================================================
INSERT INTO interaction_materials (interaction_id, material_id) VALUES
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567801', 'b1b2c3d4-e5f6-7890-abcd-ef1234567801'),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567801', 'b1b2c3d4-e5f6-7890-abcd-ef1234567802'),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567802', 'b1b2c3d4-e5f6-7890-abcd-ef1234567803'),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567803', 'b1b2c3d4-e5f6-7890-abcd-ef1234567804'),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567804', 'b1b2c3d4-e5f6-7890-abcd-ef1234567806'),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567805', 'b1b2c3d4-e5f6-7890-abcd-ef1234567809');

-- =============================================================
-- Interaction-Samples links
-- =============================================================
INSERT INTO interaction_samples (interaction_id, sample_id, quantity) VALUES
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567801', 'c1b2c3d4-e5f6-7890-abcd-ef1234567801', 5),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567802', 'c1b2c3d4-e5f6-7890-abcd-ef1234567803', 10),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567802', 'c1b2c3d4-e5f6-7890-abcd-ef1234567804', 2),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567803', 'c1b2c3d4-e5f6-7890-abcd-ef1234567805', 3),
    ('d1b2c3d4-e5f6-7890-abcd-ef1234567804', 'c1b2c3d4-e5f6-7890-abcd-ef1234567807', 10);

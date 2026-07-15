"""
Database seed script.
Populates the database with realistic sample data for development and demo.
"""

from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.doctor import Doctor
from app.models.interaction import Interaction
from app.models.material import Material
from app.models.sample import Sample

import json


def seed_database():
    """Populate database with sample data if tables are empty."""
    db: Session = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Doctor).first() is not None:
            print("Database already seeded. Skipping.")
            return

        print("Seeding database with sample data...")

        # --- Doctors ---
        doctors = [
            Doctor(name="Dr. Rajesh Sharma", hospital="Apollo Hospital, Mumbai", specialization="Cardiology", phone="+91-9876543210", email="r.sharma@apollo.com", preferred_contact="In-Person", notes="Key opinion leader in cardiac care. Prefers morning meetings."),
            Doctor(name="Dr. Priya Patel", hospital="Fortis Hospital, Delhi", specialization="Oncology", phone="+91-9876543211", email="p.patel@fortis.com", preferred_contact="Email", notes="Research-oriented. Interested in clinical trial data."),
            Doctor(name="Dr. Amit Kumar", hospital="AIIMS, Delhi", specialization="Neurology", phone="+91-9876543212", email="a.kumar@aiims.com", preferred_contact="In-Person", notes="Department head. Requires appointments 2 weeks in advance."),
            Doctor(name="Dr. Sunita Reddy", hospital="Care Hospital, Hyderabad", specialization="Endocrinology", phone="+91-9876543213", email="s.reddy@care.com", preferred_contact="Phone", notes="Diabetes specialist. High volume prescriber."),
            Doctor(name="Dr. Vikram Singh", hospital="Max Hospital, Bangalore", specialization="Orthopedics", phone="+91-9876543214", email="v.singh@max.com", preferred_contact="In-Person", notes="Sports medicine expert. Very receptive to new products."),
            Doctor(name="Dr. Anita Desai", hospital="Narayana Health, Chennai", specialization="Pediatrics", phone="+91-9876543215", email="a.desai@narayana.com", preferred_contact="Email", notes="Pediatric ICU specialist. Prefers detailed clinical data."),
            Doctor(name="Dr. Sanjay Gupta", hospital="Medanta Hospital, Gurugram", specialization="Pulmonology", phone="+91-9876543216", email="s.gupta@medanta.com", preferred_contact="Phone", notes="Asthma and COPD specialist. Active in medical conferences."),
            Doctor(name="Dr. Meera Iyer", hospital="KEM Hospital, Mumbai", specialization="Dermatology", phone="+91-9876543217", email="m.iyer@kem.com", preferred_contact="In-Person", notes="Cosmetic dermatology expert. Interested in topical formulations."),
            Doctor(name="Dr. Arjun Nair", hospital="Amrita Hospital, Kochi", specialization="Gastroenterology", phone="+91-9876543218", email="a.nair@amrita.com", preferred_contact="Email", notes="IBD specialist. Publishes frequently in journals."),
            Doctor(name="Dr. Kavita Joshi", hospital="Ruby Hall Clinic, Pune", specialization="Psychiatry", phone="+91-9876543219", email="k.joshi@ruby.com", preferred_contact="Phone", notes="Specializes in anxiety and depression. Open to new therapies."),
        ]
        db.add_all(doctors)
        db.flush()

        # --- Materials ---
        materials = [
            Material(name="CardioX Efficacy Brochure", type="Brochure", description="4-page brochure highlighting CardioX clinical trial results and efficacy data."),
            Material(name="OncoBoost Phase III Study Report", type="Clinical Study", description="Complete Phase III clinical trial report for OncoBoost showing 40% improvement in PFS."),
            Material(name="NeuroCalm Product Monograph", type="Monograph", description="Detailed product monograph for NeuroCalm including pharmacokinetics and dosing guidelines."),
            Material(name="DiabeCare Patient Education Kit", type="Patient Education", description="Patient-friendly materials explaining DiabeCare usage, diet, and lifestyle modifications."),
            Material(name="OrthoFlex Clinical Comparison", type="Clinical Study", description="Head-to-head comparison study of OrthoFlex vs. competitor products in joint pain management."),
            Material(name="PulmoAir Inhaler Technique Guide", type="Training Material", description="Step-by-step guide for proper inhaler technique with PulmoAir device."),
            Material(name="GastroEase Prescribing Information", type="Prescribing Info", description="FDA-approved prescribing information for GastroEase capsules."),
            Material(name="DermaGlow Before/After Portfolio", type="Presentation", description="Visual portfolio showing before/after results of DermaGlow treatment in clinical settings."),
        ]
        db.add_all(materials)
        db.flush()

        # --- Samples ---
        samples = [
            Sample(name="CardioX 10mg Tablets", product="CardioX", quantity=500),
            Sample(name="CardioX 25mg Tablets", product="CardioX", quantity=300),
            Sample(name="OncoBoost 50mg Capsules", product="OncoBoost", quantity=200),
            Sample(name="NeuroCalm 25mg Tablets", product="NeuroCalm", quantity=400),
            Sample(name="DiabeCare 500mg Tablets", product="DiabeCare", quantity=600),
            Sample(name="PulmoAir 200mcg Inhaler", product="PulmoAir", quantity=150),
        ]
        db.add_all(samples)
        db.flush()

        # --- Interactions ---
        interactions = [
            Interaction(
                hcp_id=doctors[0].id,
                interaction_type="Meeting",
                date="2026-07-01",
                time="10:30",
                attendees=json.dumps(["Dr. Rajesh Sharma", "Nurse Meena"]),
                topics_discussed="Discussed CardioX efficacy in treating hypertension. Doctor was impressed with Phase III trial results showing 35% reduction in cardiovascular events.",
                sentiment="Positive",
                outcomes="Doctor agreed to prescribe CardioX for new hypertension patients. Requested more clinical data on elderly patients.",
                follow_up_actions="Send elderly patient subgroup analysis by next week. Schedule follow-up in 2 weeks.",
                summary="Productive meeting with Dr. Sharma at Apollo Hospital. Presented CardioX Phase III data. Doctor expressed strong interest and agreed to trial prescriptions. Need to provide additional data for elderly patient cohort.",
                ai_generated=True,
                materials_shared=json.dumps(["CardioX Efficacy Brochure"]),
                samples_distributed=json.dumps(["CardioX 10mg Tablets"]),
            ),
            Interaction(
                hcp_id=doctors[1].id,
                interaction_type="Email",
                date="2026-07-03",
                time="14:00",
                attendees=json.dumps(["Dr. Priya Patel"]),
                topics_discussed="Shared OncoBoost Phase III study results via email. Followed up on her query about progression-free survival data.",
                sentiment="Neutral",
                outcomes="Doctor acknowledged receipt. Wants to review data before next meeting. Mentioned interest in a webinar.",
                follow_up_actions="Arrange OncoBoost webinar with KOL panel. Schedule in-person meeting after review.",
                summary="Email follow-up with Dr. Patel regarding OncoBoost clinical data. She is reviewing the Phase III report and has expressed interest in a webinar featuring key opinion leaders.",
                ai_generated=True,
                materials_shared=json.dumps(["OncoBoost Phase III Study Report"]),
                samples_distributed=json.dumps([]),
            ),
            Interaction(
                hcp_id=doctors[4].id,
                interaction_type="Conference",
                date="2026-06-28",
                time="16:00",
                attendees=json.dumps(["Dr. Vikram Singh", "Dr. Anand Mehta", "Dr. Neha Kapoor"]),
                topics_discussed="Presented OrthoFlex clinical comparison data at the Orthopedic Surgery Conference. Multiple doctors engaged in Q&A about dosing protocols.",
                sentiment="Positive",
                outcomes="Three doctors expressed interest in OrthoFlex for post-surgical pain management. Collected contact details for follow-up.",
                follow_up_actions="Send personalized follow-up emails to all three doctors. Share OrthoFlex prescribing information. Schedule individual meetings.",
                summary="Successful conference presentation on OrthoFlex. Strong reception from orthopedic surgeons with three new interested prescribers. Follow-up needed with individualized outreach.",
                ai_generated=True,
                materials_shared=json.dumps(["OrthoFlex Clinical Comparison"]),
                samples_distributed=json.dumps(["CardioX 10mg Tablets"]),
            ),
        ]
        db.add_all(interactions)

        db.commit()
        print(f"Seeded: {len(doctors)} doctors, {len(materials)} materials, {len(samples)} samples, {len(interactions)} interactions")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

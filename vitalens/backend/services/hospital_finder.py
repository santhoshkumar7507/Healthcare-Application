"""
VitaLens — services/hospital_finder.py

Dynamic hospital recommendations based on user's city.
Covers 25+ Indian cities across all major states.
Falls back gracefully to nearest city if exact match not found.
"""

from typing import List, Dict, Optional
import os

# ─────────────────────────────────────────────────────────
# HOSPITAL DATABASE
# Key: city (lowercase), Value: dict of disease → list of hospitals
# ─────────────────────────────────────────────────────────

HOSPITAL_DB: Dict[str, Dict[str, List[dict]]] = {

    # ── TAMIL NADU ─────────────────────────────────────
    "coimbatore": {
        "diabetes": [
            {"name": "Kovai Medical Center & Hospital",  "address": "99 Avanashi Road, Coimbatore 641014",       "specialty": "Diabetology & Endocrinology",     "rating": 4.7, "phone": "+91-422-4323800", "lat": 11.0168, "lng": 76.9558},
            {"name": "PSG Hospitals",                    "address": "Peelamedu, Coimbatore 641004",               "specialty": "Diabetes Clinic",                "rating": 4.6, "phone": "+91-422-4345000", "lat": 11.0241, "lng": 77.0040},
            {"name": "G. Kuppuswamy Naidu Memorial",     "address": "Nethaji Road, Coimbatore 641001",           "specialty": "Internal Medicine",              "rating": 4.5, "phone": "+91-422-2212222", "lat": 11.0022, "lng": 76.9623},
            {"name": "Sri Ramakrishna Hospital",         "address": "395 Sarojini Naidu Rd, Coimbatore 641044",  "specialty": "Endocrinology & Nephrology",      "rating": 4.6, "phone": "+91-422-4500000", "lat": 11.0139, "lng": 77.0033},
        ],
        "heart": [
            {"name": "Kovai Medical Center & Hospital",  "address": "99 Avanashi Road, Coimbatore 641014",       "specialty": "Cardiology & Cardiac Surgery",   "rating": 4.7, "phone": "+91-422-4323800", "lat": 11.0168, "lng": 76.9558},
            {"name": "Sri Ramakrishna Hospital",         "address": "395 Sarojini Naidu Rd, Coimbatore 641044",  "specialty": "Interventional Cardiology",      "rating": 4.6, "phone": "+91-422-4500000", "lat": 11.0139, "lng": 77.0033},
            {"name": "Coimbatore Medical College",       "address": "Trichy Road, Coimbatore 641018",            "specialty": "Cardiology Department",          "rating": 4.2, "phone": "+91-422-2301393", "lat": 10.9950, "lng": 76.9703},
        ],
        "hypertension": [
            {"name": "PSG Hospitals",                    "address": "Peelamedu, Coimbatore 641004",               "specialty": "Internal Medicine",              "rating": 4.6, "phone": "+91-422-4345000", "lat": 11.0241, "lng": 77.0040},
            {"name": "Kovai Medical Center & Hospital",  "address": "99 Avanashi Road, Coimbatore 641014",       "specialty": "General Medicine",               "rating": 4.7, "phone": "+91-422-4323800", "lat": 11.0168, "lng": 76.9558},
        ],
        "liver": [
            {"name": "G. Kuppuswamy Naidu Memorial",     "address": "Nethaji Road, Coimbatore 641001",           "specialty": "Gastroenterology",               "rating": 4.5, "phone": "+91-422-2212222", "lat": 11.0022, "lng": 76.9623},
            {"name": "Sri Ramakrishna Hospital",         "address": "395 Sarojini Naidu Rd, Coimbatore 641044",  "specialty": "Hepatology",                     "rating": 4.6, "phone": "+91-422-4500000", "lat": 11.0139, "lng": 77.0033},
        ],
    },

    "chennai": {
        "diabetes": [
            {"name": "Apollo Hospitals",                 "address": "21 Greams Lane, Chennai 600006",            "specialty": "Diabetology & Endocrinology",    "rating": 4.8, "phone": "+91-44-28290200",  "lat": 13.0569, "lng": 80.2525},
            {"name": "MIOT International",               "address": "4/112 Mount Poonamallee Rd, Chennai",       "specialty": "Endocrinology",                  "rating": 4.7, "phone": "+91-44-42002288",  "lat": 13.0459, "lng": 80.1758},
            {"name": "Fortis Malar Hospital",            "address": "52 First Main Rd, Adyar, Chennai 600020",   "specialty": "Diabetes & Obesity",             "rating": 4.6, "phone": "+91-44-42892222",  "lat": 13.0023, "lng": 80.2562},
            {"name": "Madras Medical College",           "address": "Park Town, Chennai 600003",                 "specialty": "Internal Medicine",              "rating": 4.3, "phone": "+91-44-25305000",  "lat": 13.0810, "lng": 80.2737},
        ],
        "heart": [
            {"name": "Apollo Hospitals",                 "address": "21 Greams Lane, Chennai 600006",            "specialty": "Cardiology & Heart Surgery",     "rating": 4.8, "phone": "+91-44-28290200",  "lat": 13.0569, "lng": 80.2525},
            {"name": "Fortis Malar Hospital",            "address": "52 First Main Rd, Adyar, Chennai 600020",   "specialty": "Cardiac Sciences",               "rating": 4.6, "phone": "+91-44-42892222",  "lat": 13.0023, "lng": 80.2562},
            {"name": "Sri Ramachandra Medical",          "address": "No 1 Ramachandra Nagar, Porur 600116",      "specialty": "Cardiothoracic Surgery",         "rating": 4.7, "phone": "+91-44-45928610",  "lat": 13.0340, "lng": 80.1574},
        ],
        "hypertension": [
            {"name": "Apollo Hospitals",                 "address": "21 Greams Lane, Chennai 600006",            "specialty": "General Medicine",               "rating": 4.8, "phone": "+91-44-28290200",  "lat": 13.0569, "lng": 80.2525},
            {"name": "MIOT International",               "address": "4/112 Mount Poonamallee Rd, Chennai",       "specialty": "Internal Medicine",              "rating": 4.7, "phone": "+91-44-42002288",  "lat": 13.0459, "lng": 80.1758},
        ],
        "liver": [
            {"name": "Global Health City",               "address": "439 Cheran Nagar, Perumbakkam 600100",      "specialty": "Hepatology & GI",                "rating": 4.7, "phone": "+91-44-44777000",  "lat": 12.9208, "lng": 80.2043},
            {"name": "Apollo Hospitals",                 "address": "21 Greams Lane, Chennai 600006",            "specialty": "Gastroenterology",               "rating": 4.8, "phone": "+91-44-28290200",  "lat": 13.0569, "lng": 80.2525},
        ],
    },

    "madurai": {
        "diabetes": [
            {"name": "Government Rajaji Hospital",       "address": "Hospital Rd, Madurai 625020",               "specialty": "General Medicine",               "rating": 4.1, "phone": "+91-452-2532535",  "lat": 9.9195,  "lng": 78.1193},
            {"name": "Meenakshi Mission Hospital",       "address": "Lake Area, Melur Rd, Madurai 625107",       "specialty": "Diabetology",                    "rating": 4.5, "phone": "+91-452-2588741",  "lat": 9.9560,  "lng": 78.1322},
        ],
        "heart": [
            {"name": "Meenakshi Mission Hospital",       "address": "Lake Area, Melur Rd, Madurai 625107",       "specialty": "Cardiology",                     "rating": 4.5, "phone": "+91-452-2588741",  "lat": 9.9560,  "lng": 78.1322},
            {"name": "Apollo Specialty Hospital",        "address": "Lake View Rd, KK Nagar, Madurai 625020",    "specialty": "Cardiac Sciences",               "rating": 4.6, "phone": "+91-452-2527777",  "lat": 9.9278,  "lng": 78.1198},
        ],
        "hypertension": [
            {"name": "Meenakshi Mission Hospital",       "address": "Lake Area, Melur Rd, Madurai 625107",       "specialty": "Internal Medicine",              "rating": 4.5, "phone": "+91-452-2588741",  "lat": 9.9560,  "lng": 78.1322},
        ],
        "liver": [
            {"name": "Apollo Specialty Hospital",        "address": "Lake View Rd, KK Nagar, Madurai 625020",    "specialty": "Gastroenterology",               "rating": 4.6, "phone": "+91-452-2527777",  "lat": 9.9278,  "lng": 78.1198},
        ],
    },

    "trichy": {
        "diabetes": [
            {"name": "Kavery Medical Center",            "address": "111 Seshapuram, Trichy 620002",             "specialty": "Diabetology",                    "rating": 4.4, "phone": "+91-431-4077777",  "lat": 10.8136, "lng": 78.6908},
            {"name": "Sri Gokulam Hospitals",            "address": "Collector Office Rd, Trichy 620001",        "specialty": "Internal Medicine",              "rating": 4.3, "phone": "+91-431-2460400",  "lat": 10.8208, "lng": 78.6867},
        ],
        "heart": [
            {"name": "Kavery Medical Center",            "address": "111 Seshapuram, Trichy 620002",             "specialty": "Cardiology",                     "rating": 4.4, "phone": "+91-431-4077777",  "lat": 10.8136, "lng": 78.6908},
        ],
        "hypertension": [
            {"name": "Sri Gokulam Hospitals",            "address": "Collector Office Rd, Trichy 620001",        "specialty": "General Medicine",               "rating": 4.3, "phone": "+91-431-2460400",  "lat": 10.8208, "lng": 78.6867},
        ],
        "liver": [
            {"name": "Kavery Medical Center",            "address": "111 Seshapuram, Trichy 620002",             "specialty": "Gastroenterology",               "rating": 4.4, "phone": "+91-431-4077777",  "lat": 10.8136, "lng": 78.6908},
        ],
    },

    "salem": {
        "diabetes": [
            {"name": "SKS Hospital",                     "address": "23 Omalur Main Rd, Salem 636004",           "specialty": "Diabetology",                    "rating": 4.4, "phone": "+91-427-2230000",  "lat": 11.6643, "lng": 78.1460},
            {"name": "Vinayaka Mission Hospital",        "address": "Sankari Main Rd, Salem 636308",             "specialty": "Internal Medicine",              "rating": 4.2, "phone": "+91-427-3919191",  "lat": 11.5964, "lng": 78.1763},
        ],
        "heart": [
            {"name": "SKS Hospital",                     "address": "23 Omalur Main Rd, Salem 636004",           "specialty": "Cardiology",                     "rating": 4.4, "phone": "+91-427-2230000",  "lat": 11.6643, "lng": 78.1460},
        ],
        "hypertension": [
            {"name": "SKS Hospital",                     "address": "23 Omalur Main Rd, Salem 636004",           "specialty": "General Medicine",               "rating": 4.4, "phone": "+91-427-2230000",  "lat": 11.6643, "lng": 78.1460},
        ],
        "liver": [
            {"name": "Vinayaka Mission Hospital",        "address": "Sankari Main Rd, Salem 636308",             "specialty": "Gastroenterology",               "rating": 4.2, "phone": "+91-427-3919191",  "lat": 11.5964, "lng": 78.1763},
        ],
    },

    # ── MAHARASHTRA ────────────────────────────────────
    "mumbai": {
        "diabetes": [
            {"name": "Lilavati Hospital",                "address": "A-791 Bandra Reclamation, Mumbai 400050",   "specialty": "Diabetology & Endocrinology",    "rating": 4.7, "phone": "+91-22-26751000",  "lat": 19.0492, "lng": 72.8278},
            {"name": "Hinduja Hospital",                 "address": "Veer Savarkar Marg, Mahim, Mumbai 400016",  "specialty": "Diabetes Clinic",                "rating": 4.6, "phone": "+91-22-24452222",  "lat": 19.0376, "lng": 72.8426},
            {"name": "Kokilaben Dhirubhai Ambani",       "address": "Four Bungalows, Andheri W, Mumbai 400053",  "specialty": "Endocrinology",                  "rating": 4.7, "phone": "+91-22-42696969",  "lat": 19.1197, "lng": 72.8315},
        ],
        "heart": [
            {"name": "Asian Heart Institute",            "address": "G/N Block, BKC, Bandra E, Mumbai 400051",   "specialty": "Cardiac Sciences",               "rating": 4.8, "phone": "+91-22-66986666",  "lat": 19.0644, "lng": 72.8652},
            {"name": "Kokilaben Dhirubhai Ambani",       "address": "Four Bungalows, Andheri W, Mumbai 400053",  "specialty": "Cardiology & Heart Surgery",     "rating": 4.7, "phone": "+91-22-42696969",  "lat": 19.1197, "lng": 72.8315},
            {"name": "Jaslok Hospital",                  "address": "15 Dr G Deshmukh Marg, Mumbai 400026",      "specialty": "Interventional Cardiology",      "rating": 4.5, "phone": "+91-22-66573333",  "lat": 18.9706, "lng": 72.8089},
        ],
        "hypertension": [
            {"name": "Hinduja Hospital",                 "address": "Veer Savarkar Marg, Mahim, Mumbai 400016",  "specialty": "General Medicine",               "rating": 4.6, "phone": "+91-22-24452222",  "lat": 19.0376, "lng": 72.8426},
            {"name": "Lilavati Hospital",                "address": "A-791 Bandra Reclamation, Mumbai 400050",   "specialty": "Internal Medicine",              "rating": 4.7, "phone": "+91-22-26751000",  "lat": 19.0492, "lng": 72.8278},
        ],
        "liver": [
            {"name": "Global Hospital",                  "address": "35 Dr E Borges Rd, Parel, Mumbai 400012",   "specialty": "Hepatology & Liver Transplant",  "rating": 4.7, "phone": "+91-22-67670101",  "lat": 18.9949, "lng": 72.8419},
            {"name": "Lilavati Hospital",                "address": "A-791 Bandra Reclamation, Mumbai 400050",   "specialty": "Gastroenterology",               "rating": 4.7, "phone": "+91-22-26751000",  "lat": 19.0492, "lng": 72.8278},
        ],
    },

    "pune": {
        "diabetes": [
            {"name": "Ruby Hall Clinic",                 "address": "40 Sassoon Rd, Pune 411001",                "specialty": "Diabetology",                    "rating": 4.6, "phone": "+91-20-26163391",  "lat": 18.5302, "lng": 73.8742},
            {"name": "Jehangir Hospital",                "address": "32 Sassoon Rd, Pune 411001",                "specialty": "Endocrinology",                  "rating": 4.5, "phone": "+91-20-26128100",  "lat": 18.5307, "lng": 73.8749},
        ],
        "heart": [
            {"name": "Ruby Hall Clinic",                 "address": "40 Sassoon Rd, Pune 411001",                "specialty": "Cardiology",                     "rating": 4.6, "phone": "+91-20-26163391",  "lat": 18.5302, "lng": 73.8742},
            {"name": "Deenanath Mangeshkar Hospital",    "address": "Erandwane, Pune 411004",                    "specialty": "Cardiac Sciences",               "rating": 4.7, "phone": "+91-20-49150100",  "lat": 18.5078, "lng": 73.8245},
        ],
        "hypertension": [
            {"name": "Jehangir Hospital",                "address": "32 Sassoon Rd, Pune 411001",                "specialty": "Internal Medicine",              "rating": 4.5, "phone": "+91-20-26128100",  "lat": 18.5307, "lng": 73.8749},
        ],
        "liver": [
            {"name": "Deenanath Mangeshkar Hospital",    "address": "Erandwane, Pune 411004",                    "specialty": "Gastroenterology",               "rating": 4.7, "phone": "+91-20-49150100",  "lat": 18.5078, "lng": 73.8245},
        ],
    },

    # ── DELHI / NCR ────────────────────────────────────
    "delhi": {
        "diabetes": [
            {"name": "AIIMS Delhi",                      "address": "Ansari Nagar East, New Delhi 110029",       "specialty": "Endocrinology & Metabolism",     "rating": 4.9, "phone": "+91-11-26588500",  "lat": 28.5672, "lng": 77.2100},
            {"name": "Max Super Speciality Hospital",    "address": "1 Press Enclave Rd, Saket, Delhi 110017",   "specialty": "Diabetology",                    "rating": 4.7, "phone": "+91-11-26515050",  "lat": 28.5244, "lng": 77.2066},
            {"name": "Fortis Hospital Vasant Kunj",      "address": "Sector B, Pocket 1, Vasant Kunj 110070",    "specialty": "Diabetes & Endocrinology",       "rating": 4.6, "phone": "+91-11-42776222",  "lat": 28.5222, "lng": 77.1573},
        ],
        "heart": [
            {"name": "Escorts Heart Institute",          "address": "Okhla Rd, New Delhi 110025",                "specialty": "Cardiac Sciences",               "rating": 4.8, "phone": "+91-11-47414141",  "lat": 28.5635, "lng": 77.2688},
            {"name": "AIIMS Delhi",                      "address": "Ansari Nagar East, New Delhi 110029",       "specialty": "Cardiology & CTVS",              "rating": 4.9, "phone": "+91-11-26588500",  "lat": 28.5672, "lng": 77.2100},
            {"name": "Max Super Speciality Hospital",    "address": "1 Press Enclave Rd, Saket, Delhi 110017",   "specialty": "Cardiology",                     "rating": 4.7, "phone": "+91-11-26515050",  "lat": 28.5244, "lng": 77.2066},
        ],
        "hypertension": [
            {"name": "AIIMS Delhi",                      "address": "Ansari Nagar East, New Delhi 110029",       "specialty": "Internal Medicine",              "rating": 4.9, "phone": "+91-11-26588500",  "lat": 28.5672, "lng": 77.2100},
            {"name": "Sir Ganga Ram Hospital",           "address": "Rajinder Nagar, New Delhi 110060",          "specialty": "General Medicine",               "rating": 4.7, "phone": "+91-11-25750000",  "lat": 28.6413, "lng": 77.1877},
        ],
        "liver": [
            {"name": "Institute of Liver & Biliary Sci","address": "D-1 Vasant Kunj, New Delhi 110070",         "specialty": "Hepatology & Liver Transplant",  "rating": 4.8, "phone": "+91-11-46300000",  "lat": 28.5204, "lng": 77.1622},
            {"name": "AIIMS Delhi",                      "address": "Ansari Nagar East, New Delhi 110029",       "specialty": "Gastroenterology",               "rating": 4.9, "phone": "+91-11-26588500",  "lat": 28.5672, "lng": 77.2100},
        ],
    },

    # ── KARNATAKA ──────────────────────────────────────
    "bangalore": {
        "diabetes": [
            {"name": "Manipal Hospitals",                "address": "98 HAL Airport Rd, Bangalore 560017",       "specialty": "Diabetology & Endocrinology",    "rating": 4.7, "phone": "+91-80-25024444",  "lat": 12.9697, "lng": 77.6484},
            {"name": "Narayana Health City",             "address": "258/A Bommasandra, Bangalore 560099",       "specialty": "Diabetes Clinic",                "rating": 4.6, "phone": "+91-80-71222222",  "lat": 12.8350, "lng": 77.6745},
            {"name": "Fortis Hospital",                  "address": "14 Cunningham Rd, Bangalore 560052",        "specialty": "Endocrinology",                  "rating": 4.6, "phone": "+91-80-66214444",  "lat": 12.9855, "lng": 77.6093},
        ],
        "heart": [
            {"name": "Narayana Health City",             "address": "258/A Bommasandra, Bangalore 560099",       "specialty": "Cardiac Sciences",               "rating": 4.6, "phone": "+91-80-71222222",  "lat": 12.8350, "lng": 77.6745},
            {"name": "Manipal Hospitals",                "address": "98 HAL Airport Rd, Bangalore 560017",       "specialty": "Cardiology",                     "rating": 4.7, "phone": "+91-80-25024444",  "lat": 12.9697, "lng": 77.6484},
            {"name": "Columbia Asia Hospital",           "address": "Kirloskar Business Park, Bangalore 560024", "specialty": "Interventional Cardiology",      "rating": 4.5, "phone": "+91-80-41794000",  "lat": 13.0184, "lng": 77.5918},
        ],
        "hypertension": [
            {"name": "Manipal Hospitals",                "address": "98 HAL Airport Rd, Bangalore 560017",       "specialty": "Internal Medicine",              "rating": 4.7, "phone": "+91-80-25024444",  "lat": 12.9697, "lng": 77.6484},
        ],
        "liver": [
            {"name": "BGS Gleneagles Global Hospital",   "address": "67 Uttarahalli Rd, Kengeri, Bangalore",    "specialty": "Hepatology",                     "rating": 4.6, "phone": "+91-80-26424000",  "lat": 12.9012, "lng": 77.5493},
        ],
    },

    "mysore": {
        "diabetes": [
            {"name": "JSS Hospital",                     "address": "MG Road, Mysore 570004",                    "specialty": "Endocrinology",                  "rating": 4.5, "phone": "+91-821-2335555",  "lat": 12.3052, "lng": 76.6551},
            {"name": "Apollo BGS Hospitals",             "address": "Adichunchanagiri Rd, Mysore 570023",        "specialty": "Diabetology",                    "rating": 4.4, "phone": "+91-821-2529990",  "lat": 12.2714, "lng": 76.6340},
        ],
        "heart": [
            {"name": "JSS Hospital",                     "address": "MG Road, Mysore 570004",                    "specialty": "Cardiology",                     "rating": 4.5, "phone": "+91-821-2335555",  "lat": 12.3052, "lng": 76.6551},
        ],
        "hypertension": [
            {"name": "Apollo BGS Hospitals",             "address": "Adichunchanagiri Rd, Mysore 570023",        "specialty": "Internal Medicine",              "rating": 4.4, "phone": "+91-821-2529990",  "lat": 12.2714, "lng": 76.6340},
        ],
        "liver": [
            {"name": "JSS Hospital",                     "address": "MG Road, Mysore 570004",                    "specialty": "Gastroenterology",               "rating": 4.5, "phone": "+91-821-2335555",  "lat": 12.3052, "lng": 76.6551},
        ],
    },

    # ── ANDHRA PRADESH / TELANGANA ─────────────────────
    "hyderabad": {
        "diabetes": [
            {"name": "Care Hospitals",                   "address": "Road 1, Banjara Hills, Hyderabad 500034",   "specialty": "Diabetology & Endocrinology",    "rating": 4.6, "phone": "+91-40-30418888",  "lat": 17.4089, "lng": 78.4379},
            {"name": "Apollo Hospitals Jubilee Hills",   "address": "Jubilee Hills, Hyderabad 500033",           "specialty": "Diabetes Clinic",                "rating": 4.7, "phone": "+91-40-23607777",  "lat": 17.4318, "lng": 78.4069},
            {"name": "NIMS — Nizam's Institute",         "address": "Punjagutta, Hyderabad 500082",              "specialty": "Endocrinology & Metabolism",     "rating": 4.5, "phone": "+91-40-23489000",  "lat": 17.4274, "lng": 78.4484},
        ],
        "heart": [
            {"name": "CARE Hospitals",                   "address": "Road 1, Banjara Hills, Hyderabad 500034",   "specialty": "Cardiology",                     "rating": 4.6, "phone": "+91-40-30418888",  "lat": 17.4089, "lng": 78.4379},
            {"name": "Star Hospitals",                   "address": "8-2-596 Rd No 10, Banjara Hills 500034",    "specialty": "Cardiac Sciences",               "rating": 4.5, "phone": "+91-40-44477777",  "lat": 17.4102, "lng": 78.4358},
        ],
        "hypertension": [
            {"name": "Apollo Hospitals Jubilee Hills",   "address": "Jubilee Hills, Hyderabad 500033",           "specialty": "Internal Medicine",              "rating": 4.7, "phone": "+91-40-23607777",  "lat": 17.4318, "lng": 78.4069},
        ],
        "liver": [
            {"name": "Asian Institute of Gastroenterology","address": "6-3-661 Somajiguda, Hyderabad 500082",   "specialty": "Hepatology & GI",                "rating": 4.8, "phone": "+91-40-23378888",  "lat": 17.4255, "lng": 78.4598},
        ],
    },

    "visakhapatnam": {
        "diabetes": [
            {"name": "KIMS Hospital",                    "address": "50-G Jagadamba Jct, Visakhapatnam 530002",  "specialty": "Diabetology",                    "rating": 4.5, "phone": "+91-891-6711000",  "lat": 17.7164, "lng": 83.3152},
            {"name": "Care Hospital",                    "address": "10-50-11/4 Waltair Uplands, Vizag 530003",  "specialty": "Endocrinology",                  "rating": 4.4, "phone": "+91-891-6662222",  "lat": 17.7276, "lng": 83.3290},
        ],
        "heart": [
            {"name": "KIMS Hospital",                    "address": "50-G Jagadamba Jct, Visakhapatnam 530002",  "specialty": "Cardiology",                     "rating": 4.5, "phone": "+91-891-6711000",  "lat": 17.7164, "lng": 83.3152},
        ],
        "hypertension": [
            {"name": "Care Hospital",                    "address": "10-50-11/4 Waltair Uplands, Vizag 530003",  "specialty": "General Medicine",               "rating": 4.4, "phone": "+91-891-6662222",  "lat": 17.7276, "lng": 83.3290},
        ],
        "liver": [
            {"name": "KIMS Hospital",                    "address": "50-G Jagadamba Jct, Visakhapatnam 530002",  "specialty": "Gastroenterology",               "rating": 4.5, "phone": "+91-891-6711000",  "lat": 17.7164, "lng": 83.3152},
        ],
    },

    # ── KERALA ─────────────────────────────────────────
    "kochi": {
        "diabetes": [
            {"name": "Amrita Institute of Medical Sciences","address": "AIMS Ponekkara, Kochi 682041",           "specialty": "Diabetology & Endocrinology",    "rating": 4.8, "phone": "+91-484-2801234",  "lat": 9.9728,  "lng": 76.2955},
            {"name": "Lakeshore Hospital",                "address": "NH 47 Nettoor, Maradu, Kochi 682304",      "specialty": "Diabetes Clinic",                "rating": 4.6, "phone": "+91-484-2701032",  "lat": 9.9565,  "lng": 76.3107},
        ],
        "heart": [
            {"name": "Amrita Institute of Medical Sciences","address": "AIMS Ponekkara, Kochi 682041",           "specialty": "Cardiology & Cardiac Surgery",   "rating": 4.8, "phone": "+91-484-2801234",  "lat": 9.9728,  "lng": 76.2955},
            {"name": "KIMS Health",                       "address": "Anayara PO, Trivandrum 695024",            "specialty": "Cardiology",                     "rating": 4.6, "phone": "+91-471-3041000",  "lat": 8.4964,  "lng": 76.9515},
        ],
        "hypertension": [
            {"name": "Lakeshore Hospital",                "address": "NH 47 Nettoor, Maradu, Kochi 682304",      "specialty": "Internal Medicine",              "rating": 4.6, "phone": "+91-484-2701032",  "lat": 9.9565,  "lng": 76.3107},
        ],
        "liver": [
            {"name": "Amrita Institute of Medical Sciences","address": "AIMS Ponekkara, Kochi 682041",           "specialty": "Hepatology",                     "rating": 4.8, "phone": "+91-484-2801234",  "lat": 9.9728,  "lng": 76.2955},
        ],
    },

    # ── WEST BENGAL ────────────────────────────────────
    "kolkata": {
        "diabetes": [
            {"name": "AMRI Hospitals",                   "address": "JC 16/17 Salt Lake, Kolkata 700098",        "specialty": "Diabetology",                    "rating": 4.5, "phone": "+91-33-66000000",  "lat": 22.5725, "lng": 88.4155},
            {"name": "Apollo Gleneagles Hospital",       "address": "58 Canal Circular Rd, Kolkata 700054",      "specialty": "Endocrinology",                  "rating": 4.6, "phone": "+91-33-23201111",  "lat": 22.5483, "lng": 88.3879},
        ],
        "heart": [
            {"name": "RN Tagore International Institute","address": "124 EM Bypass, Mukundapur, Kolkata",        "specialty": "Cardiac Sciences",               "rating": 4.7, "phone": "+91-33-66700000",  "lat": 22.5035, "lng": 88.3999},
            {"name": "Apollo Gleneagles Hospital",       "address": "58 Canal Circular Rd, Kolkata 700054",      "specialty": "Cardiology",                     "rating": 4.6, "phone": "+91-33-23201111",  "lat": 22.5483, "lng": 88.3879},
        ],
        "hypertension": [
            {"name": "AMRI Hospitals",                   "address": "JC 16/17 Salt Lake, Kolkata 700098",        "specialty": "Internal Medicine",              "rating": 4.5, "phone": "+91-33-66000000",  "lat": 22.5725, "lng": 88.4155},
        ],
        "liver": [
            {"name": "Apollo Gleneagles Hospital",       "address": "58 Canal Circular Rd, Kolkata 700054",      "specialty": "Gastroenterology",               "rating": 4.6, "phone": "+91-33-23201111",  "lat": 22.5483, "lng": 88.3879},
        ],
    },

    # ── GUJARAT ────────────────────────────────────────
    "ahmedabad": {
        "diabetes": [
            {"name": "Apollo Hospitals",                 "address": "Plot 1A GIDC, Bhat, Gandhinagar 382428",    "specialty": "Diabetology",                    "rating": 4.6, "phone": "+91-79-66701800",  "lat": 23.1671, "lng": 72.6637},
            {"name": "Sterling Hospital",                "address": "Off Gurukul Rd, Memnagar, Ahmedabad",       "specialty": "Endocrinology",                  "rating": 4.5, "phone": "+91-79-40011000",  "lat": 23.0546, "lng": 72.5490},
        ],
        "heart": [
            {"name": "UN Mehta Institute of Cardiology", "address": "Civil Hospital Campus, Ahmedabad 380016",   "specialty": "Cardiac Sciences",               "rating": 4.8, "phone": "+91-79-22681280",  "lat": 23.0391, "lng": 72.5852},
            {"name": "Apollo Hospitals",                 "address": "Plot 1A GIDC, Bhat, Gandhinagar 382428",    "specialty": "Cardiology",                     "rating": 4.6, "phone": "+91-79-66701800",  "lat": 23.1671, "lng": 72.6637},
        ],
        "hypertension": [
            {"name": "Sterling Hospital",                "address": "Off Gurukul Rd, Memnagar, Ahmedabad",       "specialty": "Internal Medicine",              "rating": 4.5, "phone": "+91-79-40011000",  "lat": 23.0546, "lng": 72.5490},
        ],
        "liver": [
            {"name": "Apollo Hospitals",                 "address": "Plot 1A GIDC, Bhat, Gandhinagar 382428",    "specialty": "Gastroenterology",               "rating": 4.6, "phone": "+91-79-66701800",  "lat": 23.1671, "lng": 72.6637},
        ],
    },

    # ── RAJASTHAN ──────────────────────────────────────
    "jaipur": {
        "diabetes": [
            {"name": "Fortis Escorts Hospital",          "address": "Jawaharlal Nehru Marg, Jaipur 302017",      "specialty": "Diabetology",                    "rating": 4.6, "phone": "+91-141-2547000",  "lat": 26.8722, "lng": 75.8141},
            {"name": "Mahatma Gandhi Hospital",          "address": "Riico Institutional Area, Jaipur 302033",   "specialty": "Endocrinology",                  "rating": 4.3, "phone": "+91-141-2212018",  "lat": 26.8637, "lng": 75.8260},
        ],
        "heart": [
            {"name": "Fortis Escorts Hospital",          "address": "Jawaharlal Nehru Marg, Jaipur 302017",      "specialty": "Cardiac Sciences",               "rating": 4.6, "phone": "+91-141-2547000",  "lat": 26.8722, "lng": 75.8141},
            {"name": "SMS Hospital",                     "address": "Sawai Ram Singh Rd, Jaipur 302004",         "specialty": "Cardiology",                     "rating": 4.4, "phone": "+91-141-2518888",  "lat": 26.9124, "lng": 75.8027},
        ],
        "hypertension": [
            {"name": "Fortis Escorts Hospital",          "address": "Jawaharlal Nehru Marg, Jaipur 302017",      "specialty": "Internal Medicine",              "rating": 4.6, "phone": "+91-141-2547000",  "lat": 26.8722, "lng": 75.8141},
        ],
        "liver": [
            {"name": "Mahatma Gandhi Hospital",          "address": "Riico Institutional Area, Jaipur 302033",   "specialty": "Gastroenterology",               "rating": 4.3, "phone": "+91-141-2212018",  "lat": 26.8637, "lng": 75.8260},
        ],
    },

    # ── UTTAR PRADESH ──────────────────────────────────
    "lucknow": {
        "diabetes": [
            {"name": "SGPGI — Sanjay Gandhi PGI",        "address": "Raebareli Rd, Lucknow 226014",              "specialty": "Endocrinology & Metabolism",     "rating": 4.7, "phone": "+91-522-2668700",  "lat": 26.7922, "lng": 80.9975},
            {"name": "Medanta Hospital Lucknow",         "address": "Sector A Pocket 1, Amar Shaheed Path",      "specialty": "Diabetology",                    "rating": 4.6, "phone": "+91-522-4505050",  "lat": 26.8418, "lng": 80.9564},
        ],
        "heart": [
            {"name": "SGPGI — Sanjay Gandhi PGI",        "address": "Raebareli Rd, Lucknow 226014",              "specialty": "Cardiology & CTVS",              "rating": 4.7, "phone": "+91-522-2668700",  "lat": 26.7922, "lng": 80.9975},
            {"name": "Medanta Hospital Lucknow",         "address": "Sector A Pocket 1, Amar Shaheed Path",      "specialty": "Cardiac Sciences",               "rating": 4.6, "phone": "+91-522-4505050",  "lat": 26.8418, "lng": 80.9564},
        ],
        "hypertension": [
            {"name": "Medanta Hospital Lucknow",         "address": "Sector A Pocket 1, Amar Shaheed Path",      "specialty": "Internal Medicine",              "rating": 4.6, "phone": "+91-522-4505050",  "lat": 26.8418, "lng": 80.9564},
        ],
        "liver": [
            {"name": "SGPGI — Sanjay Gandhi PGI",        "address": "Raebareli Rd, Lucknow 226014",              "specialty": "Gastroenterology",               "rating": 4.7, "phone": "+91-522-2668700",  "lat": 26.7922, "lng": 80.9975},
        ],
    },

    # ── PUNJAB ─────────────────────────────────────────
    "chandigarh": {
        "diabetes": [
            {"name": "PGI — PGIMER Chandigarh",          "address": "Sector 12, Chandigarh 160012",              "specialty": "Endocrinology & Metabolism",     "rating": 4.8, "phone": "+91-172-2755555",  "lat": 30.7625, "lng": 76.7750},
            {"name": "Fortis Hospital Mohali",           "address": "Phase 8, Mohali, Punjab 160059",            "specialty": "Diabetology",                    "rating": 4.6, "phone": "+91-172-4692222",  "lat": 30.7014, "lng": 76.6980},
        ],
        "heart": [
            {"name": "PGI — PGIMER Chandigarh",          "address": "Sector 12, Chandigarh 160012",              "specialty": "Cardiology & CTVS",              "rating": 4.8, "phone": "+91-172-2755555",  "lat": 30.7625, "lng": 76.7750},
            {"name": "Fortis Hospital Mohali",           "address": "Phase 8, Mohali, Punjab 160059",            "specialty": "Cardiac Sciences",               "rating": 4.6, "phone": "+91-172-4692222",  "lat": 30.7014, "lng": 76.6980},
        ],
        "hypertension": [
            {"name": "PGI — PGIMER Chandigarh",          "address": "Sector 12, Chandigarh 160012",              "specialty": "Internal Medicine",              "rating": 4.8, "phone": "+91-172-2755555",  "lat": 30.7625, "lng": 76.7750},
        ],
        "liver": [
            {"name": "PGI — PGIMER Chandigarh",          "address": "Sector 12, Chandigarh 160012",              "specialty": "Hepatology & GI",                "rating": 4.8, "phone": "+91-172-2755555",  "lat": 30.7625, "lng": 76.7750},
        ],
    },
}

# ── City aliases (common alternate names / spellings) ──
CITY_ALIASES = {
    "new delhi": "delhi",
    "ncr": "delhi",
    "bengaluru": "bangalore",
    "bombay": "mumbai",
    "calcutta": "kolkata",
    "madras": "chennai",
    "trivandrum": "kochi",
    "vizag": "visakhapatnam",
    "vizag": "visakhapatnam",
    "cbse": "coimbatore",
    "cbe": "coimbatore",
    "blr": "bangalore",
    "hyd": "hyderabad",
    "navi mumbai": "mumbai",
    "thane": "mumbai",
    "gurugram": "delhi",
    "gurgaon": "delhi",
    "noida": "delhi",
    "faridabad": "delhi",
    "nagpur": "mumbai",
    "surat": "ahmedabad",
    "vadodara": "ahmedabad",
    "ernakulam": "kochi",
    "thrissur": "kochi",
}

# ── Nearby city fallback map ───────────────────────────
NEARBY_FALLBACK = {
    "coimbatore": ["chennai", "bangalore"],
    "trichy":     ["coimbatore", "chennai"],
    "madurai":    ["coimbatore", "chennai"],
    "salem":      ["coimbatore", "chennai"],
    "mysore":     ["bangalore"],
    "kochi":      ["bangalore", "chennai"],
    "pune":       ["mumbai"],
    "nagpur":     ["mumbai"],
    "visakhapatnam": ["hyderabad"],
    "jaipur":     ["delhi"],
    "lucknow":    ["delhi"],
    "chandigarh": ["delhi"],
    "ahmedabad":  ["mumbai"],
}


def normalize_city(city: str) -> str:
    """Normalize city name for DB lookup"""
    city = city.lower().strip()
    # Remove state suffix (e.g. "Coimbatore, Tamil Nadu" → "coimbatore")
    city = city.split(",")[0].strip()
    # Check alias
    return CITY_ALIASES.get(city, city)


def find_hospitals(city: str, disease_key: str, limit: int = 4) -> List[dict]:
    """
    Find hospitals for any Indian city based on disease.
    
    Priority:
    1. Exact city match
    2. Alias match
    3. Partial string match
    4. Nearby city fallback
    5. Nearest major city (Mumbai/Delhi/Chennai/Bangalore/Hyderabad)
    """
    norm_city = normalize_city(city)
    disease_key = disease_key.lower()

    # 1. Exact match
    hospitals = HOSPITAL_DB.get(norm_city, {}).get(disease_key, [])
    if hospitals:
        return _format(hospitals[:limit], city)

    # 2. Partial string match in DB keys
    for db_city in HOSPITAL_DB:
        if db_city in norm_city or norm_city in db_city:
            hospitals = HOSPITAL_DB[db_city].get(disease_key, [])
            if hospitals:
                return _format(hospitals[:limit], city)

    # 3. Nearby city fallback
    fallbacks = NEARBY_FALLBACK.get(norm_city, [])
    for fb_city in fallbacks:
        hospitals = HOSPITAL_DB.get(fb_city, {}).get(disease_key, [])
        if hospitals:
            return _format(hospitals[:limit], city, nearby=fb_city.title())

    # 4. Nearest major metro fallback
    for major in ["mumbai", "delhi", "chennai", "bangalore", "hyderabad"]:
        hospitals = HOSPITAL_DB.get(major, {}).get(disease_key, [])
        if hospitals:
            return _format(hospitals[:limit], city, nearby=major.title())

    return []


def _format(hospitals: List[dict], user_city: str, nearby: Optional[str] = None) -> List[dict]:
    """Add is_nearby flag so frontend can show a message"""
    result = []
    for h in hospitals:
        h_copy = dict(h)
        h_copy["is_nearby"] = nearby is not None
        h_copy["nearby_city"] = nearby
        result.append(h_copy)
    return result

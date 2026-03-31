import streamlit as st
import datetime
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)

st.set_page_config(
    page_title="Bleeding Disorder Assessment Tool",
    page_icon="🩸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════════════════════════
TR = {
"English": {
  "app_title": "Bleeding Disorder Assessment Tool",
  "app_sub": "Structured clinical screening to identify bleeding disorder type and severity",
  "lang_label": "🌐 Language",
  "start_btn": "🩸  Begin Assessment",
  "patient_title": "Patient Information",
  "patient_sub": "Complete all fields before starting",
  "name_label": "Full Name", "age_label": "Age (years)", "date_label": "Assessment Date",
  "id_label": "Patient ID (optional)", "name_ph": "Enter patient name", "id_ph": "e.g. OPD-2024-001",
  "name_err": "⚠️ Patient name is required.", "age_err": "⚠️ Enter a valid age (1–120).",
  "gender_title": "Select Gender",
  "gender_sub": "Questions are tailored based on your selection",
  "male": "♂  Male", "female": "♀  Female", "other": "⚧  Other / Prefer not to say",
  "male_desc": "Includes haemophilia-specific and GU questions",
  "female_desc": "Includes menorrhagia, postpartum and pregnancy questions",
  "other_desc": "Covers broad general bleeding symptom questions",
  "q_label": "Question", "of_label": "of",
  "yes_btn": "✅  Yes", "no_btn": "❌  No",
  "back_btn": "← Back", "skip_btn": "Skip →",
  "hint_label": "Clinical note",
  "results_title": "Assessment Results",
  "results_sub": "Bleeding Disorder Classification Report",
  "positive": "Positive", "negative": "Negative", "answered": "Answered", "pattern_score": "Pattern Score",
  "likely_disorder": "Likely Disorder", "severity_label": "Severity", "workup_label": "Recommended Workup",
  "domain_breakdown": "Domain Analysis", "answer_summary": "Answer Summary",
  "no_symptoms": "✅ No significant bleeding symptoms reported across all domains.",
  "active_domains": "🔴 Active Symptom Domains",
  "disclaimer": "⚠️ Medical Disclaimer: This tool is for clinical screening only. It does not constitute a medical diagnosis. Please consult a qualified haematologist for confirmatory investigations based on ISTH BAT guidelines.",
  "retake_btn": "🔄  New Assessment", "review_btn": "← Review Answers",
  "pdf_btn": "📄  Download PDF Report", "pdf_gen": "Generating PDF...",
  "proceed_btn": "→  Enter Patient Details", "gender_next": "→  Continue",
  "gender_badge": "Gender",
  "domain_mucosal": "Mucosal Bleeding",
  "domain_skin": "Skin / Platelet",
  "domain_deep": "Deep Tissue",
  "domain_surgical": "Surgical / Procedural",
  "disorders": {
    "none":        "No Significant Bleeding Disorder",
    "vwd":         "Von Willebrand Disease (VWD)",
    "platelet":    "Platelet Function Disorder",
    "itp":         "Immune Thrombocytopenia (ITP)",
    "haemophilia": "Haemophilia A / B",
    "factor":      "Coagulation Factor Deficiency",
    "mixed":       "Mixed / Complex Bleeding Disorder",
  },
  "severities": {"none":"None","mild":"Mild","moderate":"Moderate","severe":"Severe"},
  "workups": {
    "none":        "No specific haematology workup required. Routine CBC if desired.",
    "vwd":         "VWF antigen · VWF activity (Ristocetin cofactor) · Factor VIII assay · ABO blood group · PFA-100",
    "platelet":    "CBC with peripheral smear · Platelet aggregation studies (ADP, collagen, arachidonic acid) · PFA-100 · Bleeding time",
    "itp":         "CBC · Peripheral smear for platelet morphology · Antiplatelet antibodies · Bone marrow biopsy if indicated",
    "haemophilia": "Factor VIII assay (Haemophilia A) · Factor IX assay (Haemophilia B) · APTT · Mixing studies",
    "factor":      "PT · APTT · Thrombin time · Individual factor assays (II, V, VII, X, XI, XIII)",
    "mixed":       "Full coagulation screen · Factor assays · Platelet function tests · VWF studies · CBC",
  },
  "adv_none":   "Responses suggest no significant bleeding disorder. Routine follow-up as needed.",
  "adv_vwd":    "Mucosal bleeding pattern identified. Refer to haematologist. VWF antigen, activity, and Factor VIII assay recommended.",
  "adv_platelet":"Skin and mucosal bleeding pattern. Platelet function testing and PFA-100 advised.",
  "adv_itp":    "Skin petechiae/purpura pattern with possible thrombocytopenia. CBC and bone marrow workup if indicated.",
  "adv_haemophilia": "Deep tissue and joint bleeding pattern. Urgent haematology referral. Factor VIII/IX assays required.",
  "adv_factor": "Mixed coagulation defect pattern. PT, APTT, and individual factor assays recommended.",
  "adv_mixed":  "Complex multi-domain bleeding. Urgent haematology referral for comprehensive workup.",
  "pill_q": "Questions", "pill_min": "Minutes", "pill_result": "Disorder Classification",
  "purpose_title": "Purpose", "purpose_body": "Identify likely bleeding disorder from symptom patterns",
  "instr_title": "Instructions", "instr_body": "Answer Yes or No based on personal bleeding history",
  "score_title": "Pattern Analysis", "score_body": "4 bleeding pattern domains mapped to disorder types",
  "outcome_title": "Classification", "outcome_body": "Disorder type · Severity · Recommended workup",
},

"Malayalam": {
  "app_title": "രക്തസ്രാവ ക്രമക്കേട് വിലയിരുത്തൽ ഉപകരണം",
  "app_sub": "രക്തസ്രാവ ക്രമക്കേടിന്റെ തരവും തീവ്രതയും കണ്ടെത്താൻ",
  "lang_label": "🌐 ഭാഷ",
  "start_btn": "🩸  ആരംഭിക്കുക",
  "patient_title": "രോഗി വിവരങ്ങൾ",
  "patient_sub": "ആരംഭിക്കുന്നതിന് മുമ്പ് എല്ലാ വിശദാംശങ്ങളും നൽകുക",
  "name_label": "പൂർണ്ണ നാമം", "age_label": "പ്രായം (വർഷം)", "date_label": "തീയതി",
  "id_label": "രോഗി ID (ഓപ്ഷണൽ)", "name_ph": "രോഗിയുടെ പേര്", "id_ph": "ഉദാ: OPD-2024-001",
  "name_err": "⚠️ രോഗിയുടെ പേര് ആവശ്യമാണ്.", "age_err": "⚠️ സാധുവായ പ്രായം നൽകുക (1–120).",
  "gender_title": "ലിംഗം തിരഞ്ഞെടുക്കുക",
  "gender_sub": "തിരഞ്ഞെടുപ്പ് അനുസരിച്ച് ചോദ്യങ്ങൾ ക്രമീകരിക്കും",
  "male": "♂  പുരുഷൻ", "female": "♀  സ്ത്രീ", "other": "⚧  മറ്റുള്ളവർ",
  "male_desc": "ഹീമോഫിലിയ, GU ചോദ്യങ്ങൾ ഉൾപ്പെടും",
  "female_desc": "ആർത്തവ, പ്രസവ, ഗർഭ-ബന്ധിത ചോദ്യങ്ങൾ",
  "other_desc": "പൊതു രക്തസ്രാവ ലക്ഷണ ചോദ്യങ്ങൾ",
  "q_label": "ചോദ്യം", "of_label": "/",
  "yes_btn": "✅  അതെ", "no_btn": "❌  ഇല്ല",
  "back_btn": "← തിരിച്ച്", "skip_btn": "ഒഴിവാക്കുക →",
  "hint_label": "ക്ലിനിക്കൽ കുറിപ്പ്",
  "results_title": "വിലയിരുത്തൽ ഫലങ്ങൾ",
  "results_sub": "രക്തസ്രാവ ക്രമക്കേട് വർഗ്ഗീകരണ റിപ്പോർട്ട്",
  "positive": "പോസിറ്റീവ്", "negative": "നെഗറ്റീവ്", "answered": "ഉത്തരം", "pattern_score": "രീതി സ്കോർ",
  "likely_disorder": "സംശയ ക്രമക്കേട്", "severity_label": "തീവ്രത", "workup_label": "ശുപാർശ പരിശോധനകൾ",
  "domain_breakdown": "മേഖല വിശകലനം", "answer_summary": "ഉത്തര സംഗ്രഹം",
  "no_symptoms": "✅ ഒരു മേഖലയിലും കാര്യമായ ലക്ഷണങ്ങൾ ഇല്ല.",
  "active_domains": "🔴 സജീവ ലക്ഷണ മേഖലകൾ",
  "disclaimer": "⚠️ ഈ ഉപകരണം സ്ക്രീനിംഗ് ആവശ്യങ്ങൾക്ക് മാത്രം. ഒരു ഹീമറ്റോളജിസ്റ്റുമായി ആലോചിക്കുക.",
  "retake_btn": "🔄  പുതിയ വിലയിരുത്തൽ", "review_btn": "← ചോദ്യങ്ങൾ അവലോകനം",
  "pdf_btn": "📄  PDF ഡൗൺലോഡ്", "pdf_gen": "PDF തയ്യാറാക്കുന്നു...",
  "proceed_btn": "→  വിശദാംശങ്ങൾ നൽകുക", "gender_next": "→  തുടരുക",
  "gender_badge": "ലിംഗം",
  "domain_mucosal": "മ്യൂക്കോസൽ രക്തസ്രാവം",
  "domain_skin": "ചർമ്മം / പ്ലേറ്റ്ലറ്റ്",
  "domain_deep": "ആഴമായ ടിഷ്യു",
  "domain_surgical": "ശസ്ത്രക്രിയ / നടപടിക്രമം",
  "disorders": {
    "none":        "കാര്യമായ ക്രമക്കേടില്ല",
    "vwd":         "വോൺ വില്ലെബ്രാൻഡ് രോഗം (VWD)",
    "platelet":    "പ്ലേറ്റ്ലറ്റ് ഫംഗ്ഷൻ ഡിസോർഡർ",
    "itp":         "ഇമ്മ്യൂൺ ത്രോംബോസൈറ്റോപീനിയ (ITP)",
    "haemophilia": "ഹീമോഫിലിയ A / B",
    "factor":      "ഫാക്ടർ ഡിഫിഷ്യൻസി",
    "mixed":       "മിശ്രിത / സങ്കീർണ്ണ ക്രമക്കേട്",
  },
  "severities": {"none":"ഇല്ല","mild":"നേരിയ","moderate":"മിതമായ","severe":"ഗുരുതരമായ"},
  "workups": {
    "none":        "പ്രത്യേക ഹീമറ്റോളജി പരിശോധന ആവശ്യമില്ല. CBC ഐച്ഛികം.",
    "vwd":         "VWF ആന്റിജൻ · VWF ആക്റ്റിവിറ്റി · ഫാക്ടർ VIII · ABO ഗ്രൂപ്പ് · PFA-100",
    "platelet":    "CBC · പ്ലേറ്റ്ലറ്റ് അഗ്രിഗേഷൻ (ADP, കൊളാജൻ, AA) · PFA-100 · ബ്ലീഡിംഗ് ടൈം",
    "itp":         "CBC · പ്ലേറ്റ്ലറ്റ് മോർഫോളജി · ആൻറിപ്ലേറ്റ്ലറ്റ് ആൻറിബോഡി · ബോൺ മാരോ ബയോപ്സി",
    "haemophilia": "ഫാക്ടർ VIII / IX · APTT · മിക്സിംഗ് സ്റ്റഡി",
    "factor":      "PT · APTT · ത്രോംബിൻ ടൈം · ഫാക്ടർ II/V/VII/X/XI/XIII",
    "mixed":       "കോഗുലേഷൻ സ്ക്രീൻ · ഫാക്ടർ അസ്സേ · പ്ലേറ്റ്ലറ്റ് ഫംഗ്ഷൻ · VWF പഠനങ്ങൾ · CBC",
  },
  "adv_none":   "കാര്യമായ ക്രമക്കേടിന്റെ സൂചന ഇല്ല. ആവശ്യമെങ്കിൽ ഫോളോ-അപ്പ്.",
  "adv_vwd":    "മ്യൂക്കോസൽ രീതി. ഹീമറ്റോളജിസ്റ്റ് റഫറൽ. VWF ആന്റിജൻ, ആക്റ്റിവിറ്റി ശുപാർശ.",
  "adv_platelet":"ചർമ്മ, മ്യൂക്കോസൽ രീതി. PFA-100 ഉം പ്ലേറ്റ്ലറ്റ് അഗ്രിഗേഷനും ശുപാർശ.",
  "adv_itp":    "ചർമ്മ പർപ്പൂര/പിറ്റേക്കിയ രീതി. CBC, ആൻറിബോഡി, ബോൺ മാരോ ശുപാർശ.",
  "adv_haemophilia": "ആഴമായ ടിഷ്യൂ/സന്ധി രീതി. അടിയന്തിര ഹീമറ്റോളജി. ഫാക്ടർ VIII/IX ആവശ്യം.",
  "adv_factor": "മിശ്രിത കോഗുലേഷൻ ക്രമക്കേട്. PT, APTT, ഫാക്ടർ അസ്സേ ശുപാർശ.",
  "adv_mixed":  "സങ്കീർണ്ണ ബഹു-മേഖല രക്തസ്രാവം. അടിയന്തിര ഹീമറ്റോളജി റഫറൽ.",
  "pill_q": "ചോദ്യങ്ങൾ", "pill_min": "മിനിറ്റ്", "pill_result": "ക്രമക്കേട് വർഗ്ഗീകരണം",
  "purpose_title": "ലക്ഷ്യം", "purpose_body": "ലക്ഷണ രീതിയിൽ നിന്ന് ക്രമക്കേട് കണ്ടെത്തുക",
  "instr_title": "നിർദ്ദേശങ്ങൾ", "instr_body": "വ്യക്തിഗത ചരിത്രം അടിസ്ഥാനമാക്കി ഉത്തരം",
  "score_title": "രീതി വിശകലനം", "score_body": "4 മേഖലകൾ ക്രമക്കേടുകളുമായി ബന്ധിപ്പിച്ചിരിക്കുന്നു",
  "outcome_title": "വർഗ്ഗീകരണം", "outcome_body": "ക്രമക്കേട് · തീവ്രത · പരിശോധനകൾ",
},

"Hindi": {
  "app_title": "रक्तस्राव विकार मूल्यांकन उपकरण",
  "app_sub": "रक्तस्राव विकार का प्रकार और गंभीरता पहचानने के लिए",
  "lang_label": "🌐 भाषा",
  "start_btn": "🩸  मूल्यांकन शुरू करें",
  "patient_title": "रोगी जानकारी",
  "patient_sub": "शुरू करने से पहले सभी विवरण भरें",
  "name_label": "पूरा नाम", "age_label": "आयु (वर्ष)", "date_label": "तिथि",
  "id_label": "रोगी ID (वैकल्पिक)", "name_ph": "रोगी का नाम", "id_ph": "जैसे OPD-2024-001",
  "name_err": "⚠️ रोगी का नाम आवश्यक है।", "age_err": "⚠️ वैध आयु दर्ज करें (1–120)।",
  "gender_title": "लिंग चुनें",
  "gender_sub": "आपके चयन के अनुसार प्रश्न अनुकूलित होंगे",
  "male": "♂  पुरुष", "female": "♀  महिला", "other": "⚧  अन्य",
  "male_desc": "हीमोफिलिया और GU प्रश्न शामिल होंगे",
  "female_desc": "मासिक धर्म, प्रसव, गर्भावस्था प्रश्न शामिल होंगे",
  "other_desc": "सामान्य रक्तस्राव लक्षण प्रश्न",
  "q_label": "प्रश्न", "of_label": "/",
  "yes_btn": "✅  हाँ", "no_btn": "❌  नहीं",
  "back_btn": "← वापस", "skip_btn": "छोड़ें →",
  "hint_label": "नैदानिक टिप्पणी",
  "results_title": "मूल्यांकन परिणाम",
  "results_sub": "रक्तस्राव विकार वर्गीकरण रिपोर्ट",
  "positive": "सकारात्मक", "negative": "नकारात्मक", "answered": "उत्तर दिए", "pattern_score": "पैटर्न स्कोर",
  "likely_disorder": "संभावित विकार", "severity_label": "गंभीरता", "workup_label": "अनुशंसित जांच",
  "domain_breakdown": "डोमेन विश्लेषण", "answer_summary": "उत्तर सारांश",
  "no_symptoms": "✅ किसी भी डोमेन में कोई महत्वपूर्ण लक्षण नहीं।",
  "active_domains": "🔴 सक्रिय लक्षण डोमेन",
  "disclaimer": "⚠️ यह उपकरण केवल स्क्रीनिंग के लिए है। यह चिकित्सा निदान नहीं है। हेमेटोलॉजिस्ट से परामर्श करें।",
  "retake_btn": "🔄  नया मूल्यांकन", "review_btn": "← प्रश्न समीक्षा",
  "pdf_btn": "📄  PDF डाउनलोड", "pdf_gen": "PDF बन रही है...",
  "proceed_btn": "→  रोगी जानकारी दर्ज करें", "gender_next": "→  जारी रखें",
  "gender_badge": "लिंग",
  "domain_mucosal": "म्यूकोसल रक्तस्राव",
  "domain_skin": "त्वचा / प्लेटलेट",
  "domain_deep": "गहरे ऊतक",
  "domain_surgical": "सर्जिकल / प्रक्रियात्मक",
  "disorders": {
    "none":        "कोई महत्वपूर्ण रक्तस्राव विकार नहीं",
    "vwd":         "वॉन विलेब्रांड रोग (VWD)",
    "platelet":    "प्लेटलेट फंक्शन विकार",
    "itp":         "इम्यून थ्रोम्बोसाइटोपेनिया (ITP)",
    "haemophilia": "हीमोफिलिया A / B",
    "factor":      "कोएगुलेशन फैक्टर की कमी",
    "mixed":       "मिश्रित / जटिल रक्तस्राव विकार",
  },
  "severities": {"none":"कोई नहीं","mild":"हल्का","moderate":"मध्यम","severe":"गंभीर"},
  "workups": {
    "none":        "कोई विशेष हेमेटोलॉजी जांच आवश्यक नहीं। इच्छित हो तो CBC।",
    "vwd":         "VWF एंटीजन · VWF एक्टिविटी · फैक्टर VIII · ABO ग्रुप · PFA-100",
    "platelet":    "CBC · प्लेटलेट एग्रीगेशन (ADP, कोलेजन, AA) · PFA-100 · ब्लीडिंग टाइम",
    "itp":         "CBC · प्लेटलेट मॉर्फोलॉजी · एंटीप्लेटलेट एंटीबॉडी · बोन मैरो बायोप्सी",
    "haemophilia": "फैक्टर VIII / IX · APTT · मिक्सिंग स्टडी",
    "factor":      "PT · APTT · थ्रोम्बिन टाइम · फैक्टर II/V/VII/X/XI/XIII",
    "mixed":       "पूर्ण कोएगुलेशन स्क्रीन · फैक्टर असेस · प्लेटलेट फंक्शन · VWF · CBC",
  },
  "adv_none":   "कोई महत्वपूर्ण विकार नहीं। आवश्यकतानुसार फॉलो-अप।",
  "adv_vwd":    "म्यूकोसल पैटर्न। हेमेटोलॉजिस्ट रेफरल। VWF एंटीजन, एक्टिविटी अनुशंसित।",
  "adv_platelet":"त्वचा और म्यूकोसल पैटर्न। PFA-100 और प्लेटलेट एग्रीगेशन सलाह।",
  "adv_itp":    "पर्पुरा/पेटेकिया पैटर्न। CBC, एंटीबॉडी, बोन मैरो जांच।",
  "adv_haemophilia": "गहरे ऊतक/जोड़ पैटर्न। तत्काल हेमेटोलॉजी। फैक्टर VIII/IX आवश्यक।",
  "adv_factor": "मिश्रित कोएगुलेशन दोष। PT, APTT, व्यक्तिगत फैक्टर असेस।",
  "adv_mixed":  "जटिल बहु-डोमेन रक्तस्राव। तत्काल हेमेटोलॉजी रेफरल।",
  "pill_q": "प्रश्न", "pill_min": "मिनट", "pill_result": "विकार वर्गीकरण",
  "purpose_title": "उद्देश्य", "purpose_body": "लक्षण पैटर्न से विकार की पहचान",
  "instr_title": "निर्देश", "instr_body": "व्यक्तिगत इतिहास के आधार पर उत्तर दें",
  "score_title": "पैटर्न विश्लेषण", "score_body": "4 डोमेन विकार प्रकारों से जुड़े हैं",
  "outcome_title": "वर्गीकरण", "outcome_body": "विकार · गंभीरता · जांच",
},

"Tamil": {
  "app_title": "இரத்தப்போக்கு கோளாறு மதிப்பீட்டு கருவி",
  "app_sub": "இரத்தப்போக்கு கோளாறு வகை மற்றும் தீவிரத்தை கண்டறிய",
  "lang_label": "🌐 மொழி",
  "start_btn": "🩸  தொடங்கவும்",
  "patient_title": "நோயாளர் தகவல்",
  "patient_sub": "தொடங்குவதற்கு முன் அனைத்து விவரங்களையும் நிரப்பவும்",
  "name_label": "முழு பெயர்", "age_label": "வயது (ஆண்டுகள்)", "date_label": "தேதி",
  "id_label": "நோயாளர் ID (விருப்பமானால்)", "name_ph": "நோயாளரின் பெயர்", "id_ph": "எ.கா. OPD-2024-001",
  "name_err": "⚠️ நோயாளரின் பெயர் தேவை.", "age_err": "⚠️ சரியான வயதை உள்ளிடவும் (1–120).",
  "gender_title": "பாலினத்தை தேர்ந்தெடுக்கவும்",
  "gender_sub": "உங்கள் தேர்வின் படி கேள்விகள் தனிப்பயனாக்கப்படும்",
  "male": "♂  ஆண்", "female": "♀  பெண்", "other": "⚧  மற்றவர்கள்",
  "male_desc": "ஹீமோஃபிலியா மற்றும் GU கேள்விகள் உட்பட",
  "female_desc": "மாதவிடாய், பிரசவம், கர்ப்பகால கேள்விகள்",
  "other_desc": "பொது இரத்தப்போக்கு அறிகுறி கேள்விகள்",
  "q_label": "கேள்வி", "of_label": "/",
  "yes_btn": "✅  ஆம்", "no_btn": "❌  இல்லை",
  "back_btn": "← திரும்பு", "skip_btn": "தவிர் →",
  "hint_label": "மருத்துவ குறிப்பு",
  "results_title": "மதிப்பீட்டு முடிவுகள்",
  "results_sub": "இரத்தப்போக்கு கோளாறு வகைப்பாடு அறிக்கை",
  "positive": "நேர்மறை", "negative": "எதிர்மறை", "answered": "பதிலளித்தது", "pattern_score": "வடிவ மதிப்பெண்",
  "likely_disorder": "சாத்தியமான கோளாறு", "severity_label": "தீவிரம்", "workup_label": "பரிந்துரைக்கப்பட்ட பரிசோதனைகள்",
  "domain_breakdown": "பகுதி பகுப்பாய்வு", "answer_summary": "பதில் சுருக்கம்",
  "no_symptoms": "✅ எந்த பகுதியிலும் குறிப்பிடத்தக்க அறிகுறிகள் இல்லை.",
  "active_domains": "🔴 செயலில் உள்ள அறிகுறி பகுதிகள்",
  "disclaimer": "⚠️ இந்த கருவி திரையிடல் நோக்கங்களுக்காக மட்டுமே. தகுதிவாய்ந்த ஹேமட்டாலஜிஸ்ட்டை அணுகவும்.",
  "retake_btn": "🔄  புதிய மதிப்பீடு", "review_btn": "← கேள்விகளை மதிப்பாய்வு",
  "pdf_btn": "📄  PDF பதிவிறக்கம்", "pdf_gen": "PDF உருவாக்கப்படுகிறது...",
  "proceed_btn": "→  நோயாளர் தகவலை உள்ளிடவும்", "gender_next": "→  தொடரவும்",
  "gender_badge": "பாலினம்",
  "domain_mucosal": "சளி சவ்வு இரத்தம்",
  "domain_skin": "தோல் / பிளேட்லெட்",
  "domain_deep": "ஆழமான திசு",
  "domain_surgical": "அறுவை சிகிச்சை / செயல்முறை",
  "disorders": {
    "none":        "குறிப்பிடத்தக்க கோளாறு இல்லை",
    "vwd":         "வான் வில்லேப்ராண்ட் நோய் (VWD)",
    "platelet":    "பிளேட்லெட் செயல்பாடு கோளாறு",
    "itp":         "இம்யூன் த்ரோம்போசைட்டோபீனியா (ITP)",
    "haemophilia": "ஹீமோஃபிலியா A / B",
    "factor":      "உறைதல் காரணி குறைபாடு",
    "mixed":       "கலவை / சிக்கலான கோளாறு",
  },
  "severities": {"none":"இல்லை","mild":"லேசான","moderate":"மிதமான","severe":"கடுமையான"},
  "workups": {
    "none":        "சிறப்பு ஹேமட்டாலஜி பரிசோதனை தேவையில்லை. விரும்பினால் CBC.",
    "vwd":         "VWF ஆன்டிஜன் · VWF செயல்பாடு · காரணி VIII · ABO குரூப் · PFA-100",
    "platelet":    "CBC · பிளேட்லெட் திரட்டல் (ADP, கொலாஜன், AA) · PFA-100 · ரத்தப்போக்கு நேரம்",
    "itp":         "CBC · பிளேட்லெட் உருவியல் · எதிர்பிளேட்லெட் ஆன்டிபாடி · எலும்பு மஜ்ஜை பயாப்ஸி",
    "haemophilia": "காரணி VIII / IX · APTT · கலப்பு ஆய்வு",
    "factor":      "PT · APTT · த்ரோம்பின் நேரம் · காரணி II/V/VII/X/XI/XIII",
    "mixed":       "முழு உறைதல் திரையிடல் · காரணி ஆய்வு · பிளேட்லெட் செயல்பாடு · VWF · CBC",
  },
  "adv_none":   "குறிப்பிடத்தக்க கோளாறு இல்லை. தேவைப்பட்டால் பின்தொடர்தல்.",
  "adv_vwd":    "சளிச்சவ்வு வடிவம். ஹேமட்டாலஜிஸ்ட் பரிந்துரை. VWF ஆன்டிஜன், செயல்பாடு பரிந்துரை.",
  "adv_platelet":"தோல் மற்றும் சளிச்சவ்வு வடிவம். PFA-100 மற்றும் பிளேட்லெட் திரட்டல் ஆலோசனை.",
  "adv_itp":    "பர்புரா/பெட்டிக்கியா வடிவம். CBC, ஆன்டிபாடி, எலும்பு மஜ்ஜை பரிசோதனை.",
  "adv_haemophilia": "ஆழமான திசு/மூட்டு வடிவம். அவசர ஹேமட்டாலஜி. காரணி VIII/IX தேவை.",
  "adv_factor": "கலவை உறைதல் குறைபாடு. PT, APTT, காரணி ஆய்வு பரிந்துரை.",
  "adv_mixed":  "சிக்கலான பல-பகுதி இரத்தப்போக்கு. அவசர ஹேமட்டாலஜி பரிந்துரை.",
  "pill_q": "கேள்விகள்", "pill_min": "நிமிடங்கள்", "pill_result": "கோளாறு வகைப்பாடு",
  "purpose_title": "நோக்கம்", "purpose_body": "அறிகுறி வடிவத்தில் இருந்து கோளாறை கண்டறிய",
  "instr_title": "வழிமுறைகள்", "instr_body": "தனிப்பட்ட வரலாற்றின் படி பதிலளிக்கவும்",
  "score_title": "வடிவ பகுப்பாய்வு", "score_body": "4 பகுதிகள் கோளாறு வகைகளுடன் இணைக்கப்பட்டுள்ளன",
  "outcome_title": "வகைப்பாடு", "outcome_body": "கோளாறு · தீவிரம் · பரிசோதனைகள்",
},
}

# ══════════════════════════════════════════════════════════════════════════════
#  QUESTION BANK  (domain: mucosal | skin | deep | surgical)
#  disorder_hint drives the classification algorithm
#  weight 1–3
# ══════════════════════════════════════════════════════════════════════════════
QUESTIONS = {
"English": [
  # ─── MUCOSAL ──────────────────────────────────────────────────────────────
  {"id":1,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"Epistaxis",
   "text":"Do you have frequent or prolonged nosebleeds lasting more than 10 minutes, or recurring more than once a month?",
   "hint":"Recurrent spontaneous epistaxis is a hallmark of VWD and platelet disorders — key mucosal bleeding feature"},
  {"id":2,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"Oral / Gum Bleeding",
   "text":"Do your gums bleed spontaneously or with minimal pressure such as gentle tooth-brushing?",
   "hint":"Gum bleeding without dental disease strongly suggests a primary haemostasis defect — VWD or platelet dysfunction"},
  {"id":3,"gender":"all","domain":"mucosal","disorder_hint":"mixed","weight":2,"category":"GI Bleeding",
   "text":"Have you ever had unexplained blood in your stools or been diagnosed with gastrointestinal bleeding without a structural cause?",
   "hint":"Mucosal GI bleeding without structural cause suggests VWD, platelet disorder, or HHT"},
  {"id":4,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":1,"category":"Haematuria",
   "text":"Have you noticed blood in your urine on more than one occasion, without a urinary infection or kidney stones?",
   "hint":"Recurrent unexplained haematuria can be a feature of VWD or platelet dysfunction"},
  {"id":5,"gender":"female","domain":"mucosal","disorder_hint":"vwd","weight":3,"category":"Menorrhagia",
   "text":"Do you have heavy menstrual bleeding — periods lasting more than 7 days, or needing to change a pad or tampon every 1–2 hours?",
   "hint":"Heavy menstrual bleeding since menarche is the most common presenting symptom of VWD in women"},
  # ─── SKIN / PLATELET ──────────────────────────────────────────────────────
  {"id":6,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"Petechiae",
   "text":"Do you develop pinpoint red or purple spots on your skin (petechiae) that appear without any injury, especially on the legs or feet?",
   "hint":"Petechiae without trauma are the hallmark of thrombocytopenia — most characteristic of ITP"},
  {"id":7,"gender":"all","domain":"skin","disorder_hint":"platelet","weight":2,"category":"Easy Bruising",
   "text":"Do you bruise easily and spontaneously, forming bruises larger than a 5-rupee coin without significant trauma?",
   "hint":"Spontaneous large bruises suggest platelet dysfunction or VWD — common in primary haemostasis defects"},
  {"id":8,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"Purpura",
   "text":"Have you ever developed widespread purple patches on your skin (purpura) appearing without injury?",
   "hint":"Purpura without trauma is characteristic of severe thrombocytopenia — ITP or drug-induced"},
  # ─── DEEP TISSUE ──────────────────────────────────────────────────────────
  {"id":9,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"Haemarthrosis",
   "text":"Have you ever had bleeding into a joint — knee, elbow, or ankle — causing pain, warmth, and swelling without significant injury?",
   "hint":"Spontaneous haemarthrosis is the pathognomonic feature of haemophilia A or B — secondary haemostasis defect"},
  {"id":10,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"Muscle Haematoma",
   "text":"Have you ever had a deep bleed inside a muscle (muscle haematoma) without significant trauma?",
   "hint":"Spontaneous muscle haematomas are highly specific for severe haemophilia — particularly iliopsoas and thigh"},
  {"id":11,"gender":"all","domain":"deep","disorder_hint":"factor","weight":3,"category":"Intracranial Bleeding",
   "text":"Have you ever had a spontaneous bleed inside or around the brain, not related to a head injury?",
   "hint":"Spontaneous ICH is an emergency — raises strong suspicion for severe haemophilia or rare factor deficiency"},
  {"id":12,"gender":"male","domain":"deep","disorder_hint":"haemophilia","weight":2,"category":"Family History — Male Pattern",
   "text":"Do any male relatives (father, brother, uncle, maternal grandfather) have a history of severe bleeding into joints or muscles?",
   "hint":"X-linked recessive inheritance — haemophilia A and B are carried by females and predominantly affect males"},
  # ─── SURGICAL / PROCEDURAL ────────────────────────────────────────────────
  {"id":13,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":2,"category":"Post-Surgical Bleeding",
   "text":"Have you had excessive bleeding after a surgical procedure that required re-operation, prolonged packing, or a blood transfusion?",
   "hint":"Post-operative bleeding needing intervention is strongly suggestive of an underlying coagulation defect"},
  {"id":14,"gender":"all","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"Post-Dental Bleeding",
   "text":"Did you bleed for more than 30 minutes or require a hospital visit after a tooth extraction or dental procedure?",
   "hint":"Prolonged post-dental bleeding is a sensitive early indicator of VWD and platelet function disorders"},
  {"id":15,"gender":"all","domain":"surgical","disorder_hint":"factor","weight":2,"category":"Transfusion for Bleeding",
   "text":"Have you ever required a blood transfusion specifically because of a bleeding episode (not routine surgical blood loss)?",
   "hint":"Bleeding requiring transfusion indicates clinically significant haemostatic failure — investigate thoroughly"},
  {"id":16,"gender":"female","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"Postpartum Haemorrhage",
   "text":"Have you ever had excessive bleeding after childbirth requiring a blood transfusion, uterine packing, or prolonged hospitalisation?",
   "hint":"Postpartum haemorrhage is a major presentation of VWD and platelet disorders — often first diagnosis trigger"},
  {"id":17,"gender":"male","domain":"surgical","disorder_hint":"haemophilia","weight":2,"category":"Post-Circumcision Bleeding",
   "text":"Did you have excessive or prolonged bleeding after circumcision that required medical attention or re-admission?",
   "hint":"Post-circumcision bleeding is a classic early clinical clue for haemophilia in male infants and children"},
  {"id":18,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":1,"category":"Wound Bleeding",
   "text":"Do minor cuts or wounds take more than 15 minutes to stop bleeding, even with direct pressure applied?",
   "hint":"Prolonged bleeding from minor wounds is a non-specific but important screening indicator of haemostatic defect"},
  # ─── GENERAL CROSS-DOMAIN ─────────────────────────────────────────────────
  {"id":19,"gender":"all","domain":"mucosal","disorder_hint":"itp","weight":1,"category":"Iron Deficiency Anaemia",
   "text":"Have you been treated for iron-deficiency anaemia caused by ongoing or recurrent bleeding from any site?",
   "hint":"Chronic blood-loss anaemia often reflects significant mucosal or menstrual bleeding — VWD, ITP, platelet disorders"},
  {"id":20,"gender":"all","domain":"skin","disorder_hint":"mixed","weight":1,"category":"Family Bleeding History",
   "text":"Has a close family member (parent, sibling, or child) been diagnosed with a bleeding disorder such as haemophilia, VWD, or a platelet disorder?",
   "hint":"Positive family history significantly raises pre-test probability for an inherited bleeding disorder"},
],

"Malayalam": [
  {"id":1,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"മൂക്കിൽ നിന്ന് രക്തം",
   "text":"10 മിനിറ്റിൽ കൂടുതൽ നീണ്ടുനിൽക്കുന്ന അല്ലെങ്കിൽ മാസത്തിൽ ഒന്നിലധികം തവണ മൂക്കിൽ നിന്ന് രക്തം വരുന്നുണ്ടോ?",
   "hint":"VWD, പ്ലേറ്റ്ലറ്റ് ക്രമക്കേടിന്റെ പ്രധാന ലക്ഷണം"},
  {"id":2,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"മോണ രക്തസ്രാവം",
   "text":"ദന്ത ബ്രഷ് ചെയ്യുമ്പോൾ അല്ലെങ്കിൽ ലഘുവായ സ്പർശനത്തിൽ മോണ രക്തം ഉണ്ടാകുന്നുണ്ടോ?",
   "hint":"ദന്ത രോഗം ഇല്ലാതെ മോണ രക്തം — VWF ക്രമക്കേടിന്റെ സൂചന"},
  {"id":3,"gender":"all","domain":"mucosal","disorder_hint":"mixed","weight":2,"category":"ദഹന രക്തസ്രാവം",
   "text":"ഘടനാപരമായ കാരണം ഇല്ലാതെ മലത്തിൽ രക്തം ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"VWD, പ്ലേറ്റ്ലറ്റ് ക്രമക്കേട്, HHT-യുടെ സൂചന"},
  {"id":4,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":1,"category":"മൂത്രത്തിൽ രക്തം",
   "text":"മൂത്ര അണുബാധ ഇല്ലാതെ ഒന്നിലധികം തവണ മൂത്രത്തിൽ രക്തം ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"VWD അല്ലെങ്കിൽ പ്ലേറ്റ്ലറ്റ് ഡിസ്ഫംഗ്ഷന്റെ ലക്ഷണം"},
  {"id":5,"gender":"female","domain":"mucosal","disorder_hint":"vwd","weight":3,"category":"ആർത്തവ രക്തസ്രാവം",
   "text":"7 ദിവസത്തിൽ കൂടുതൽ ആർത്തവം അല്ലെങ്കിൽ ഓരോ 1–2 മണിക്കൂറിലും പ്യാഡ് മാറ്റേണ്ടി വരുന്നുണ്ടോ?",
   "hint":"സ്ത്രീകളിൽ VWD-ന്റെ ഏറ്റവും സാധാരണ ലക്ഷണം"},
  {"id":6,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"ചർമ്മ പൊട്ടൽ (Petechiae)",
   "text":"ആഘാതം ഇല്ലാതെ ചർമ്മത്തിൽ ചെറിയ ചുവന്ന/ധൂമ്ര ബിന്ദുക്കൾ (petechiae) ഉണ്ടാകുന്നുണ്ടോ?",
   "hint":"ITP-ന്റെ നിർണ്ണായക ലക്ഷണം — ത്രോംബോസൈറ്റോപീനിയ"},
  {"id":7,"gender":"all","domain":"skin","disorder_hint":"platelet","weight":2,"category":"ചതവ്",
   "text":"കാര്യമായ ആഘാതം ഇല്ലാതെ വലിയ ചതവ് ഉണ്ടാകുന്നുണ്ടോ?",
   "hint":"പ്ലേറ്റ്ലറ്റ് ഡിസ്ഫംഗ്ഷൻ, VWD-ന്റെ ലക്ഷണം"},
  {"id":8,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"പർപ്പൂര (Purpura)",
   "text":"ആഘാതം ഇല്ലാതെ ചർമ്മത്തിൽ വ്യാപകമായ ധൂമ്ര പാടുകൾ ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"ITP, ഗുരുതരമായ ത്രോംബോസൈറ്റോപീനിയ"},
  {"id":9,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"സന്ധി രക്തസ്രാവം",
   "text":"കാര്യമായ ആഘാതം ഇല്ലാതെ മുട്ട്, കൈമുട്ട്, കണങ്കൈ സന്ധിയിൽ വേദനയും നീർക്കെട്ടും ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"ഹീമോഫിലിയ A/B-ന്റെ നിർണ്ണായക ലക്ഷണം"},
  {"id":10,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"പേശി ഹിമാറ്റോമ",
   "text":"കാര്യമായ ആഘാതം ഇല്ലാതെ പേശിക്കകത്ത് ആഴത്തിലുള്ള രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"ഹീമോഫിലിയയ്ക്ക് ഉയർന്ന നിർദ്ദിഷ്ടത"},
  {"id":11,"gender":"all","domain":"deep","disorder_hint":"factor","weight":3,"category":"തലയ്ക്കകത്ത് രക്തസ്രാവം",
   "text":"ആഘാതവുമായി ബന്ധമില്ലാതെ തലച്ചോറിനുള്ളിൽ/ചുറ്റും രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"ഗുരുതരമായ ഫാക്ടർ ഡിഫിഷ്യൻസി, ഹീമോഫിലിയ"},
  {"id":12,"gender":"male","domain":"deep","disorder_hint":"haemophilia","weight":2,"category":"ഹീമോഫിലിയ കുടുംബ ചരിത്രം",
   "text":"ആൺ ബന്ധുക്കൾക്ക് (അച്ഛൻ, സഹോദരൻ, അമ്മാവൻ) സന്ധി/പേശി രക്തസ്രാവ ചരിത്രം ഉണ്ടോ?",
   "hint":"X-ലിങ്ക്ഡ് ഇൻഹെറിറ്റൻസ് — ഹീമോഫിലിയ A, B"},
  {"id":13,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":2,"category":"ശസ്ത്രക്രിയ",
   "text":"ഒരു ശസ്ത്രക്രിയ ശേഷം പുനഃ ഓപ്പറേഷൻ, രക്തം മാറ്റൽ ആവശ്യമായ അമിത രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"ഹോമോസ്റ്റേസിസ് ക്രമക്കേടിന്റെ ശക്തമായ സൂചന"},
  {"id":14,"gender":"all","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"ദന്ത ചികിത്സ",
   "text":"പല്ല് പിഴുതെടുത്ത ശേഷം 30 മിനിറ്റിൽ കൂടുതൽ രക്തം ഒഴുകി ആശുപത്രി സഹായം ആവശ്യമായിട്ടുണ്ടോ?",
   "hint":"VWD, പ്ലേറ്റ്ലറ്റ് ക്രമക്കേടിന്റെ ആദ്യ സൂചന"},
  {"id":15,"gender":"all","domain":"surgical","disorder_hint":"factor","weight":2,"category":"രക്തം മാറ്റൽ",
   "text":"ആസൂത്രിത ശസ്ത്രക്രിയ അല്ലാതെ, രക്തസ്രാവം കാരണം മാത്രം രക്തം മാറ്റൽ ആവശ്യമായിട്ടുണ്ടോ?",
   "hint":"ഗുരുതരമായ ഹോമോസ്റ്റേറ്റിക് ക്രമക്കേടിന്റെ സൂചന"},
  {"id":16,"gender":"female","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"പ്രസവ രക്തസ്രാവം",
   "text":"പ്രസവ ശേഷം ട്രാൻസ്ഫ്യൂഷൻ ആവശ്യമായ അമിത രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"VWD, പ്ലേറ്റ്ലറ്റ് ക്രമക്കേടിന്റെ പ്രധാന ലക്ഷണം"},
  {"id":17,"gender":"male","domain":"surgical","disorder_hint":"haemophilia","weight":2,"category":"ഖതനം",
   "text":"ഖതനം ശേഷം വൈദ്യ ശ്രദ്ധ ആവശ്യമായ അമിത/ദീർഘ രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
   "hint":"ആൺ കുഞ്ഞുങ്ങളിൽ ഹീമോഫിലിയ ആദ്യ ലക്ഷണം"},
  {"id":18,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":1,"category":"മുറിവ്",
   "text":"നേരിട്ട് ശ്രദ്ധ നൽകിയിട്ടും ചെറിയ മുറിവുകൾ 15 മിനിറ്റിൽ കൂടുതൽ രക്തം ഒഴുകുന്നുണ്ടോ?",
   "hint":"ഹോമോസ്റ്റേറ്റിക് ദൗർബല്യത്തിന്റെ ലക്ഷണം"},
  {"id":19,"gender":"all","domain":"mucosal","disorder_hint":"itp","weight":1,"category":"ഇരുമ്പ് കുറവ് അനിമിയ",
   "text":"ആവർത്തിക്കുന്ന രക്തസ്രാവം കാരണം ഇരുമ്പ് കുറവ് അനിമിയ ഉണ്ടോ?",
   "hint":"VWD, ITP, പ്ലേറ്റ്ലറ്റ് ക്രമക്കേടിന്റെ ലക്ഷണം"},
  {"id":20,"gender":"all","domain":"skin","disorder_hint":"mixed","weight":1,"category":"കുടുംബ ചരിത്രം",
   "text":"ഒരു അടുത്ത കുടുംബ അംഗത്തിന് ഹീമോഫിലിയ, VWD, അല്ലെങ്കിൽ പ്ലേറ്റ്ലറ്റ് ക്രമക്കേട് ഉണ്ടോ?",
   "hint":"ജന്മനിൽ ക്രമക്കേടിന്റെ സാധ്യത ഉയർത്തുന്നു"},
],

"Hindi": [
  {"id":1,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"नाक से खून",
   "text":"क्या 10 मिनट से अधिक या महीने में एक से ज़्यादा बार नाक से खून आता है?",
   "hint":"VWD और प्लेटलेट विकार की प्रमुख विशेषता"},
  {"id":2,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"मसूड़ों से खून",
   "text":"क्या हल्के दबाव या ब्रश करने से मसूड़ों से खून आता है?",
   "hint":"बिना दंत रोग के मसूड़ों से खून — VWF दोष का संकेत"},
  {"id":3,"gender":"all","domain":"mucosal","disorder_hint":"mixed","weight":2,"category":"पाचन रक्तस्राव",
   "text":"क्या संरचनात्मक कारण के बिना मल में खून आया है?",
   "hint":"VWD, प्लेटलेट विकार, HHT का संकेत"},
  {"id":4,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":1,"category":"पेशाब में खून",
   "text":"क्या संक्रमण के बिना एक से अधिक बार पेशाब में खून आया है?",
   "hint":"VWD या प्लेटलेट डिसफंक्शन का लक्षण"},
  {"id":5,"gender":"female","domain":"mucosal","disorder_hint":"vwd","weight":3,"category":"मासिक धर्म रक्तस्राव",
   "text":"क्या मासिक धर्म 7 दिन से अधिक रहता है या हर 1–2 घंटे में पैड बदलना पड़ता है?",
   "hint":"महिलाओं में VWD की सबसे आम प्रस्तुति"},
  {"id":6,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"पेटेकिया",
   "text":"क्या बिना चोट के त्वचा पर छोटे लाल/बैंगनी बिंदु (petechiae) दिखते हैं?",
   "hint":"ITP का प्रमुख लक्षण — थ्रोम्बोसाइटोपेनिया"},
  {"id":7,"gender":"all","domain":"skin","disorder_hint":"platelet","weight":2,"category":"आसान चोट",
   "text":"क्या बिना चोट के बड़े निशान बन जाते हैं?",
   "hint":"प्लेटलेट डिसफंक्शन, VWD का लक्षण"},
  {"id":8,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"पर्पुरा",
   "text":"क्या बिना चोट के त्वचा पर बड़े बैंगनी धब्बे हुए हैं?",
   "hint":"ITP, गंभीर थ्रोम्बोसाइटोपेनिया"},
  {"id":9,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"जोड़ों में खून",
   "text":"क्या बिना चोट के घुटने, कोहनी, टखने में दर्द और सूजन के साथ रक्तस्राव हुआ है?",
   "hint":"हीमोफिलिया A/B का विशिष्ट लक्षण"},
  {"id":10,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"मांसपेशी में खून",
   "text":"क्या बिना आघात के मांसपेशी के अंदर गहरा रक्तस्राव हुआ है?",
   "hint":"हीमोफिलिया के लिए उच्च विशिष्टता"},
  {"id":11,"gender":"all","domain":"deep","disorder_hint":"factor","weight":3,"category":"मस्तिष्क रक्तस्राव",
   "text":"क्या सिर की चोट के बिना मस्तिष्क में रक्तस्राव हुआ है?",
   "hint":"गंभीर फैक्टर कमी, हीमोफिलिया — आपातकाल"},
  {"id":12,"gender":"male","domain":"deep","disorder_hint":"haemophilia","weight":2,"category":"हीमोफिलिया पारिवारिक इतिहास",
   "text":"क्या पुरुष रिश्तेदारों (पिता, भाई, चाचा) को जोड़ों/मांसपेशियों में रक्तस्राव की समस्या है?",
   "hint":"X-लिंक्ड विरासत — हीमोफिलिया A, B"},
  {"id":13,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":2,"category":"सर्जरी के बाद खून",
   "text":"क्या सर्जरी के बाद पुनः ऑपरेशन या रक्त चढ़ाने की आवश्यकता पड़ी?",
   "hint":"हेमोस्टेसिस विफलता का संकेत"},
  {"id":14,"gender":"all","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"दंत प्रक्रिया",
   "text":"क्या दांत निकालने के बाद 30 मिनट से अधिक खून आया या अस्पताल जाना पड़ा?",
   "hint":"VWD, प्लेटलेट विकार की पहचान"},
  {"id":15,"gender":"all","domain":"surgical","disorder_hint":"factor","weight":2,"category":"रक्त आधान",
   "text":"क्या नियोजित सर्जरी के बिना, केवल रक्तस्राव के कारण रक्त चढ़ाना पड़ा?",
   "hint":"गंभीर हेमोस्टेटिक विफलता"},
  {"id":16,"gender":"female","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"प्रसव रक्तस्राव",
   "text":"क्या प्रसव के बाद रक्त चढ़ाने की आवश्यकता वाला अत्यधिक रक्तस्राव हुआ?",
   "hint":"VWD, प्लेटलेट विकार की प्रमुख प्रस्तुति"},
  {"id":17,"gender":"male","domain":"surgical","disorder_hint":"haemophilia","weight":2,"category":"खतना",
   "text":"क्या खतने के बाद चिकित्सा ध्यान की आवश्यकता वाला रक्तस्राव हुआ?",
   "hint":"पुरुष शिशुओं में हीमोफिलिया का प्रारंभिक संकेत"},
  {"id":18,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":1,"category":"घाव",
   "text":"क्या दबाव देने पर भी छोटे घावों से 15 मिनट से अधिक खून बहता है?",
   "hint":"हेमोस्टेटिक दुर्बलता का संकेत"},
  {"id":19,"gender":"all","domain":"mucosal","disorder_hint":"itp","weight":1,"category":"एनीमिया",
   "text":"क्या बार-बार रक्तस्राव के कारण आयरन की कमी से एनीमिया हुआ है?",
   "hint":"VWD, ITP, प्लेटलेट विकार का लक्षण"},
  {"id":20,"gender":"all","domain":"skin","disorder_hint":"mixed","weight":1,"category":"पारिवारिक इतिहास",
   "text":"क्या किसी करीबी परिवार के सदस्य को हीमोफिलिया, VWD या प्लेटलेट विकार है?",
   "hint":"वंशानुगत रक्तस्राव विकार की संभावना बढ़ाता है"},
],

"Tamil": [
  {"id":1,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"மூக்கிலிருந்து இரத்தம்",
   "text":"10 நிமிடங்களுக்கும் அதிகமாக அல்லது மாதத்தில் ஒரு முறைக்கும் மேல் மூக்கிலிருந்து இரத்தம் வருகிறதா?",
   "hint":"VWD மற்றும் பிளேட்லெட் கோளாறின் முக்கிய அறிகுறி"},
  {"id":2,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":2,"category":"ஈறு இரத்தம்",
   "text":"பல் துலக்கும்போது அல்லது லேசான அழுத்தத்தில் ஈறுகளிலிருந்து இரத்தம் வருகிறதா?",
   "hint":"பல் நோய் இல்லாமல் ஈறு இரத்தம் — VWF குறைபாடு"},
  {"id":3,"gender":"all","domain":"mucosal","disorder_hint":"mixed","weight":2,"category":"குடல் இரத்தம்",
   "text":"கட்டமைப்பு காரணம் இல்லாமல் மலத்தில் இரத்தம் வந்ததுண்டா?",
   "hint":"VWD, பிளேட்லெட் கோளாறு, HHT அறிகுறி"},
  {"id":4,"gender":"all","domain":"mucosal","disorder_hint":"vwd","weight":1,"category":"சிறுநீரில் இரத்தம்",
   "text":"தொற்று இல்லாமல் ஒன்றுக்கு மேற்பட்ட முறை சிறுநீரில் இரத்தம் வந்ததுண்டா?",
   "hint":"VWD அல்லது பிளேட்லெட் செயலிழப்பு"},
  {"id":5,"gender":"female","domain":"mucosal","disorder_hint":"vwd","weight":3,"category":"மாதவிடாய் இரத்தம்",
   "text":"மாதவிடாய் 7 நாட்களுக்கும் அதிகமாக இருக்கிறதா அல்லது ஒவ்வொரு 1–2 மணி நேரத்திலும் நாப்கின் மாற்ற வேண்டுமா?",
   "hint":"பெண்களில் VWD-ன் மிகவும் பொதுவான வெளிப்பாடு"},
  {"id":6,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"பெட்டிக்கியா",
   "text":"காயம் இல்லாமல் தோலில் சிறிய சிவப்பு/ஊதா புள்ளிகள் (petechiae) தோன்றுகின்றனவா?",
   "hint":"ITP-ன் முக்கிய அறிகுறி — த்ரோம்போசைட்டோபீனியா"},
  {"id":7,"gender":"all","domain":"skin","disorder_hint":"platelet","weight":2,"category":"காயங்கள்",
   "text":"கடுமையான அதிர்ச்சி இல்லாமல் பெரிய காயங்கள் ஏற்படுகின்றனவா?",
   "hint":"பிளேட்லெட் செயலிழப்பு, VWD அறிகுறி"},
  {"id":8,"gender":"all","domain":"skin","disorder_hint":"itp","weight":3,"category":"பர்புரா",
   "text":"காயம் இல்லாமல் தோலில் பரவலான ஊதா நிற திட்டுகள் தோன்றியதுண்டா?",
   "hint":"ITP, கடுமையான த்ரோம்போசைட்டோபீனியா"},
  {"id":9,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"மூட்டு இரத்தம்",
   "text":"கடுமையான அதிர்ச்சி இல்லாமல் முழங்கால், முழங்கை மூட்டில் வலி மற்றும் வீக்கத்துடன் இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
   "hint":"ஹீமோஃபிலியா A/B-ன் தனிச்சிறப்பு அறிகுறி"},
  {"id":10,"gender":"all","domain":"deep","disorder_hint":"haemophilia","weight":3,"category":"தசை ரத்தக்கட்டு",
   "text":"கடுமையான அதிர்ச்சி இல்லாமல் தசைக்குள் ஆழமான இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
   "hint":"ஹீமோஃபிலியாவிற்கு அதிக குறிப்பிட்டது"},
  {"id":11,"gender":"all","domain":"deep","disorder_hint":"factor","weight":3,"category":"மூளை இரத்தம்",
   "text":"தலையில் அடிபடாமல் மூளையில் இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
   "hint":"கடுமையான காரணி குறைபாடு, ஹீமோஃபிலியா — அவசரநிலை"},
  {"id":12,"gender":"male","domain":"deep","disorder_hint":"haemophilia","weight":2,"category":"ஹீமோஃபிலியா வரலாறு",
   "text":"ஆண் உறவினர்களுக்கு (தந்தை, சகோதரர், மாமா) மூட்டு/தசை இரத்தப்போக்கு வரலாறு உள்ளதா?",
   "hint":"X-இணைப்பு மரபு — ஹீமோஃபிலியா A, B"},
  {"id":13,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":2,"category":"அறுவை சிகிச்சை",
   "text":"அறுவை சிகிச்சைக்கு பிறகு மீண்டும் அறுவை சிகிச்சை அல்லது இரத்தம் ஏற்றல் தேவைப்பட்டதுண்டா?",
   "hint":"ஹீமோஸ்டேசிஸ் தோல்வியின் அறிகுறி"},
  {"id":14,"gender":"all","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"பல் சிகிச்சை",
   "text":"பல் பிடுங்கிய பிறகு 30 நிமிடங்களுக்கும் அதிகமாக இரத்தம் வந்து மருத்துவமனை சென்றதுண்டா?",
   "hint":"VWD, பிளேட்லெட் கோளாறின் ஆரம்ப அறிகுறி"},
  {"id":15,"gender":"all","domain":"surgical","disorder_hint":"factor","weight":2,"category":"இரத்தம் ஏற்றல்",
   "text":"திட்டமிட்ட அறுவை சிகிச்சை அல்லாமல், இரத்தப்போக்கு மட்டுமே காரணமாக இரத்தம் ஏற்றல் தேவைப்பட்டதுண்டா?",
   "hint":"கடுமையான ஹீமோஸ்டேடிக் தோல்வி"},
  {"id":16,"gender":"female","domain":"surgical","disorder_hint":"vwd","weight":2,"category":"பிரசவ இரத்தம்",
   "text":"பிரசவத்திற்கு பிறகு இரத்தம் ஏற்றல் தேவைப்பட்ட அதிகப்படியான இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
   "hint":"VWD, பிளேட்லெட் கோளாறின் முக்கிய வெளிப்பாடு"},
  {"id":17,"gender":"male","domain":"surgical","disorder_hint":"haemophilia","weight":2,"category":"விருத்தசேதனம்",
   "text":"விருத்தசேதனத்திற்கு பிறகு மருத்துவ கவனிப்பு தேவைப்பட்ட அதிக இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
   "hint":"ஆண் குழந்தைகளில் ஹீமோஃபிலியாவின் ஆரம்ப அறிகுறி"},
  {"id":18,"gender":"all","domain":"surgical","disorder_hint":"mixed","weight":1,"category":"காயம்",
   "text":"நேரடி அழுத்தம் கொடுத்தாலும் சிறிய காயங்கள் 15 நிமிடங்களுக்கும் அதிகமாக இரத்தம் வருகிறதா?",
   "hint":"ஹீமோஸ்டேடிக் பலவீனத்தின் அறிகுறி"},
  {"id":19,"gender":"all","domain":"mucosal","disorder_hint":"itp","weight":1,"category":"இரும்புச்சத்து குறைபாடு",
   "text":"மீண்டும் மீண்டும் வரும் இரத்தப்போக்கு காரணமாக இரும்புச்சத்து குறைபாடு உள்ளதா?",
   "hint":"VWD, ITP, பிளேட்லெட் கோளாறின் அறிகுறி"},
  {"id":20,"gender":"all","domain":"skin","disorder_hint":"mixed","weight":1,"category":"குடும்ப வரலாறு",
   "text":"நெருங்கிய குடும்ப உறுப்பினருக்கு ஹீமோஃபிலியா, VWD அல்லது பிளேட்லெட் கோளாறு உள்ளதா?",
   "hint":"பரம்பரை கோளாறின் சாத்தியத்தை அதிகரிக்கிறது"},
],
}

# ══════════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,500&display=swap');
:root {
  --bg: #04080f; --s1: #0b1220; --s2: #111c2e; --s3: #172238;
  --border: #1e3050; --accent: #38bdf8; --accent2: #818cf8;
  --red: #f43f5e; --amber: #f59e0b; --green: #34d399; --purple: #a78bfa;
  --text: #e2e8f0; --muted: #64748b; --light: #94a3b8;
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"]>section,
[data-testid="block-container"], .main, .block-container {
  background: var(--bg) !important; color: var(--text) !important;
}
[data-testid="stHeader"] { background: var(--bg) !important; }
*, p, span, div, label { font-family: 'DM Sans', sans-serif !important; color: var(--text); }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* Progress */
.stProgress > div > div > div {
  background: linear-gradient(90deg, var(--accent2), var(--accent)) !important;
  border-radius: 99px; box-shadow: 0 0 10px rgba(56,189,248,.4);
}
.stProgress > div > div { background: var(--s2) !important; border-radius: 99px; height: 7px !important; }

/* Buttons */
div.stButton > button {
  font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
  font-size: .92rem !important; border-radius: 10px !important; padding: .6rem 1.4rem !important;
  border: 1px solid var(--border) !important; background: var(--s2) !important;
  color: var(--text) !important; transition: all .18s ease !important;
}
div.stButton > button:hover {
  background: var(--s3) !important; border-color: var(--accent) !important;
  color: var(--accent) !important; transform: translateY(-2px) !important;
}
div.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #0e4f6e, var(--accent)) !important;
  border: none !important; color: #fff !important;
}
div.stButton > button[kind="primary"]:hover {
  background: linear-gradient(135deg, var(--accent), #0e4f6e) !important;
  color: #fff !important; transform: translateY(-3px) !important;
}

/* Cards */
.card {
  background: var(--s1); border: 1px solid var(--border); border-radius: 18px;
  padding: 1.8rem 1.6rem; margin-bottom: 1.2rem; position: relative; overflow: hidden;
  box-shadow: 0 4px 30px rgba(0,0,0,.5);
}
.card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}

/* Hero */
.hero { text-align: center; padding: 2rem 1rem .5rem; }
.hero-icon { font-size: 3.2rem; filter: drop-shadow(0 0 18px rgba(244,63,94,.7));
  animation: throb 2.4s ease-in-out infinite; display: block; margin-bottom: .3rem; }
@keyframes throb { 0%,100%{transform:scale(1)} 50%{transform:scale(1.07)} }
.hero-title { font-family: 'Playfair Display', serif !important; font-size: 2.3rem !important;
  font-weight: 700 !important; margin: .2rem 0 .5rem !important; line-height: 1.2 !important;
  background: linear-gradient(135deg, #e2e8f0 20%, var(--accent));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-sub { color: var(--muted) !important; font-size: .95rem; max-width: 480px;
  margin: 0 auto 1.5rem; line-height: 1.6; }
.pills { display: flex; gap: .5rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.8rem; }
.pill { background: var(--s2); border: 1px solid var(--border); border-radius: 99px;
  padding: .3rem .9rem; font-size: .8rem; color: var(--muted) !important; }
.pill b { color: var(--accent) !important; }

/* Info grid */
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; }
.info-box { background: var(--s2); border: 1px solid var(--border); border-radius: 12px;
  padding: .9rem 1rem; }
.info-icon { font-size: 1.2rem; margin-bottom: .35rem; }
.info-title { font-weight: 600; font-size: .88rem; margin-bottom: .2rem; }
.info-body { color: var(--muted) !important; font-size: .8rem; line-height: 1.5; }

/* Section label */
.section-label { text-align: center; padding: 1.2rem 0 .8rem; }
.section-icon { font-size: 2.2rem; }
.section-title { font-family: 'Playfair Display', serif !important; font-size: 1.6rem !important;
  margin: .2rem 0 .3rem !important; }
.section-sub { color: var(--muted) !important; font-size: .88rem; }

/* Gender cards */
.gender-card { background: var(--s2); border: 1px solid var(--border); border-radius: 14px;
  padding: 1rem 1.2rem; margin-bottom: .6rem; display: flex; align-items: center; gap: 1rem; }
.gender-icon { font-size: 2rem; width: 2.8rem; text-align: center; }
.gender-name { font-weight: 700; font-size: .95rem; margin-bottom: .15rem; }
.gender-desc { color: var(--muted) !important; font-size: .8rem; }

/* Question area */
.step-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: .4rem; }
.step-left { color: var(--muted) !important; font-size: .8rem; }
.step-right { color: var(--accent) !important; font-size: .8rem; font-weight: 700; }
.q-domain { display: inline-flex; align-items: center; gap: .4rem; background: var(--s3);
  border-radius: 99px; padding: .2rem .8rem; font-size: .74rem; font-weight: 600;
  color: var(--accent2) !important; border: 1px solid var(--border); margin-bottom: .7rem; }
.q-text { font-family: 'Playfair Display', serif !important; font-size: 1.45rem !important;
  line-height: 1.45 !important; color: var(--text) !important; margin-bottom: .7rem !important; }
.q-hint { font-size: .82rem; color: var(--muted) !important; background: var(--s2);
  border-left: 3px solid var(--accent); border-radius: 0 8px 8px 0; padding: .5rem .9rem; }
.divider { border: none; height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent); margin: .9rem 0; }
.pt-strip { background: var(--s2); border: 1px solid var(--border); border-radius: 10px;
  padding: .55rem 1.1rem; margin-bottom: .8rem; display: flex; gap: 1.6rem; flex-wrap: wrap; }
.pt-item { font-size: .79rem; color: var(--muted) !important; }
.pt-item strong { color: var(--accent) !important; }

/* Dot nav */
.dots { display: flex; gap: 5px; justify-content: center; margin-top: 1.2rem; flex-wrap: wrap; }
.dot { width: 9px; height: 9px; border-radius: 50%; }

/* Results */
.stat-row { display: flex; justify-content: space-around; background: var(--s2);
  border: 1px solid var(--border); border-radius: 14px; padding: .9rem; margin-bottom: 1rem; }
.stat-item { text-align: center; }
.stat-val { font-family: 'Playfair Display', serif !important; font-size: 1.7rem !important;
  font-weight: 700 !important; line-height: 1 !important; }
.stat-lbl { font-size: .73rem; color: var(--muted) !important; margin-top: .15rem; }

/* Domain breakdown */
.domain-row { display: flex; align-items: center; gap: .8rem; padding: .55rem 0;
  border-bottom: 1px solid var(--border); }
.domain-row:last-child { border-bottom: none; }
.domain-name { flex: 1; font-size: .88rem; font-weight: 500; }
.domain-bar-bg { flex: 2; background: var(--s3); border-radius: 99px; height: 7px; overflow: hidden; }
.domain-bar-fill { height: 100%; border-radius: 99px; }
.domain-score { min-width: 2.5rem; text-align: right; font-size: .82rem;
  font-weight: 700; color: var(--accent) !important; }

/* Result card */
.result-card { text-align: center; border-radius: 18px; padding: 1.8rem 1.4rem;
  border: 1px solid; margin-bottom: 1rem; }
.disorder-name { font-family: 'Playfair Display', serif !important;
  font-size: 1.6rem !important; font-weight: 700 !important; margin: .5rem 0 .3rem !important; }
.severity-pill { display: inline-flex; align-items: center; gap: .4rem;
  border-radius: 99px; padding: .35rem 1.1rem; font-weight: 700; font-size: .9rem;
  margin-bottom: .8rem; }
.workup-box { background: rgba(0,0,0,.3); border-radius: 10px; padding: .9rem 1.1rem;
  font-size: .85rem; color: var(--light) !important; text-align: left; line-height: 1.7; }
.workup-label { font-size: .72rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--accent) !important; margin-bottom: .35rem; }
.answer-row { display: flex; align-items: flex-start; gap: .7rem; padding: .55rem 0;
  border-bottom: 1px solid var(--border); font-size: .86rem; }
.answer-row:last-child { border-bottom: none; }
.ans-num { min-width: 2rem; color: var(--muted) !important; font-size: .74rem;
  font-weight: 600; padding-top: .1rem; }
.ans-cat { min-width: 5.5rem; font-size: .74rem; font-weight: 600;
  color: var(--accent2) !important; padding-top: .05rem; }
.ans-text { flex: 1; color: var(--light) !important; line-height: 1.4; }
.ans-val { min-width: 3rem; text-align: right; font-weight: 700; font-size: .86rem; }
.disclaimer-box { background: linear-gradient(135deg, #1c1a05, #271f00);
  border: 1px solid #ca8a04; border-radius: 12px; padding: .9rem 1.1rem;
  font-size: .82rem; color: #fbbf24 !important; margin-top: 1.4rem; line-height: 1.5; }

/* Input overrides */
div[data-baseweb="select"] > div {
  background: var(--s2) !important; border-color: var(--border) !important;
  color: var(--text) !important; border-radius: 10px !important;
}
div[data-baseweb="select"] * { color: var(--text) !important; }
div[data-baseweb="popover"] * { background: var(--s1) !important; color: var(--text) !important; }
input[type="text"], input[type="number"], .stTextInput input, .stNumberInput input,
.stDateInput input {
  background: var(--s2) !important; border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: 10px !important;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
GENDER_MAP = {
    "♂  Male":"male","♀  Female":"female","⚧  Other / Prefer not to say":"other",
    "♂  പുരുഷൻ":"male","♀  സ്ത്രീ":"female","⚧  മറ്റുള്ളവർ":"other",
    "♂  पुरुष":"male","♀  महिला":"female","⚧  अन्य":"other",
    "♂  ஆண்":"male","♀  பெண்":"female","⚧  மற்றவர்கள்":"other",
}

def get_questions(lang, gender_label):
    gk   = GENDER_MAP.get(gender_label, "other")
    pool = QUESTIONS.get(lang, QUESTIONS["English"])
    return [q for q in pool if q["gender"] == "all"] + \
           [q for q in pool if q["gender"] == gk]


def classify(questions, answers, t):
    """
    Score each disorder type based on weighted yes answers per disorder_hint.
    Domain scores feed severity.
    Returns dict with disorder key, severity key, domain scores.
    """
    disorder_scores = {d: 0 for d in ["vwd","platelet","itp","haemophilia","factor","mixed"]}
    domain_scores   = {d: 0 for d in ["mucosal","skin","deep","surgical"]}
    domain_max      = {d: 0 for d in ["mucosal","skin","deep","surgical"]}

    for i, q in enumerate(questions):
        domain_max[q["domain"]] += q["weight"]
        if answers.get(i) == "Yes":
            domain_scores[q["domain"]] += q["weight"]
            hint = q["disorder_hint"]
            if hint == "mixed":
                for dk in disorder_scores: disorder_scores[dk] += q["weight"] * 0.4
            else:
                disorder_scores[hint]   += q["weight"] * 2.0
                disorder_scores["mixed"] += q["weight"] * 0.3

    total_yes_weight = sum(q["weight"] for i,q in enumerate(questions) if answers.get(i)=="Yes")

    # Determine primary disorder
    if total_yes_weight == 0:
        return {"disorder":"none","severity":"none","domain_scores":domain_scores,
                "domain_max":domain_max,"total_yes_weight":0,
                "advice":t["adv_none"],"workup":t["workups"]["none"]}

    best = max(disorder_scores, key=lambda k: disorder_scores[k])

    # Tie-break: prefer specificity
    top_score = disorder_scores[best]
    candidates = [k for k,v in disorder_scores.items() if v >= top_score * 0.85]
    if len(candidates) > 1:
        if "haemophilia" in candidates and domain_scores["deep"] > 0: best = "haemophilia"
        elif "itp" in candidates and domain_scores["skin"] > domain_scores["mucosal"]: best = "itp"
        elif "vwd" in candidates and domain_scores["mucosal"] > domain_scores["skin"]: best = "vwd"
        elif "mixed" in candidates: best = "mixed"

    # Severity based on total weighted yes score
    if total_yes_weight <= 2:   sev = "mild"
    elif total_yes_weight <= 5: sev = "moderate"
    else:                       sev = "severe"

    # Special escalation: deep tissue always ≥ moderate
    if domain_scores["deep"] > 0 and sev == "mild": sev = "moderate"
    # ICH present → severe
    for i,q in enumerate(questions):
        if q.get("category","").lower() in ("intracranial bleeding","तलयककत रकतसरव",
           "തലയ്ക്കകത്ത് രക്തം","மூளை இரத்தம்") and answers.get(i)=="Yes":
            sev = "severe"; break

    adv_key    = f"adv_{best}"
    return {
        "disorder": best, "severity": sev,
        "domain_scores": domain_scores, "domain_max": domain_max,
        "total_yes_weight": total_yes_weight,
        "advice": t.get(adv_key, t["adv_mixed"]),
        "workup": t["workups"][best],
    }


DISORDER_STYLE = {
    "none":        {"color":"#34d399","bg":"linear-gradient(135deg,#022c22,#064e3b)","icon":"✅","border":"#34d39944"},
    "vwd":         {"color":"#38bdf8","bg":"linear-gradient(135deg,#082030,#0c3a58)","icon":"💧","border":"#38bdf844"},
    "platelet":    {"color":"#818cf8","bg":"linear-gradient(135deg,#12102e,#1e1b4b)","icon":"🩹","border":"#818cf844"},
    "itp":         {"color":"#f59e0b","bg":"linear-gradient(135deg,#1c1005,#292100)","icon":"⚠️","border":"#f59e0b44"},
    "haemophilia": {"color":"#f43f5e","bg":"linear-gradient(135deg,#1f0a10,#4c0519)","icon":"🩸","border":"#f43f5e44"},
    "factor":      {"color":"#a78bfa","bg":"linear-gradient(135deg,#1a0a2e,#3b0764)","icon":"🔬","border":"#a78bfa44"},
    "mixed":       {"color":"#fb923c","bg":"linear-gradient(135deg,#1f1005,#431407)","icon":"🔴","border":"#fb923c44"},
}
SEVERITY_COLOR = {"none":"#34d399","mild":"#38bdf8","moderate":"#f59e0b","severe":"#f43f5e"}
DOMAIN_COLOR   = {"mucosal":"#38bdf8","skin":"#818cf8","deep":"#f43f5e","surgical":"#f59e0b"}
DOMAIN_ICON    = {"mucosal":"💧","skin":"🩹","deep":"🦴","surgical":"🔧"}


def make_chart(questions, answers, domain_scores, domain_max, result, t):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    fig.patch.set_facecolor("#0b1220")
    c_main = DISORDER_STYLE[result["disorder"]]["color"]

    # ── 1. Donut yes/no
    ax = axes[0]; ax.set_facecolor("#0b1220")
    yes_c = sum(1 for v in answers.values() if v=="Yes")
    no_c  = sum(1 for v in answers.values() if v=="No")
    sk_c  = len(answers) - yes_c - no_c
    sizes  = [s for s in [yes_c, no_c, sk_c] if s > 0]
    cols   = [c_main, "#34d399", "#1e3050"]
    labels = [t["positive"], t["negative"], "—"]
    used_c = [cols[i] for i,s in enumerate([yes_c,no_c,sk_c]) if s>0]
    used_l = [labels[i] for i,s in enumerate([yes_c,no_c,sk_c]) if s>0]
    ax.pie(sizes, colors=used_c, startangle=90,
           wedgeprops=dict(width=0.52, edgecolor="#0b1220", linewidth=2))
    ax.text(0, 0.1, str(yes_c), ha="center", va="center", fontsize=22, fontweight="bold", color=c_main)
    ax.text(0, -0.22, f"{t['of_label']} {len(answers)}", ha="center", va="center", fontsize=10, color="#64748b")
    ax.set_title(t["positive"]+" / "+t["negative"], color="#e2e8f0", fontsize=10, pad=8)
    patches = [mpatches.Patch(color=used_c[i], label=used_l[i]) for i in range(len(sizes))]
    ax.legend(handles=patches, loc="lower center", fontsize=8,
              facecolor="#111c2e", edgecolor="#1e3050", labelcolor="#e2e8f0",
              ncol=len(patches), bbox_to_anchor=(0.5,-0.1))

    # ── 2. Radar / domain bar
    ax2 = axes[1]; ax2.set_facecolor("#0b1220")
    doms  = ["mucosal","skin","deep","surgical"]
    d_labels = [t.get(f"domain_{d}", d) for d in doms]
    scores = [domain_scores[d] for d in doms]
    maxes  = [max(domain_max[d],1) for d in doms]
    pcts   = [s/m for s,m in zip(scores,maxes)]
    d_cols = [DOMAIN_COLOR[d] for d in doms]
    bars   = ax2.barh(d_labels, pcts, color=d_cols, height=0.5,
                      edgecolor="#0b1220", linewidth=0.5)
    ax2.set_xlim(0,1.1); ax2.set_xticks([0,.5,1])
    ax2.set_xticklabels(["0%","50%","100%"], color="#64748b", fontsize=8)
    ax2.tick_params(colors="#94a3b8", labelsize=8)
    for sp in ax2.spines.values(): sp.set_color("#1e3050")
    for lbl in ax2.get_yticklabels(): lbl.set_color("#94a3b8")
    ax2.set_facecolor("#0b1220")
    ax2.set_title(t["domain_breakdown"], color="#e2e8f0", fontsize=10, pad=8)
    for bar, pct, dc in zip(bars, pcts, d_cols):
        ax2.text(pct+0.03, bar.get_y()+bar.get_height()/2,
                 f"{pct*100:.0f}%", va="center", fontsize=8, color=dc)

    # ── 3. Disorder likelihood gauge
    ax3 = axes[2]; ax3.set_facecolor("#0b1220"); ax3.axis("off")
    disorders_show = ["vwd","platelet","itp","haemophilia","factor","mixed"]
    disorder_labels = [t["disorders"][d] for d in disorders_show]
    # Compute simple display scores from domain pattern
    d_scores_display = {
        "vwd":         (domain_scores["mucosal"]*2 + domain_scores["surgical"]) / max(1, domain_max["mucosal"]*2+domain_max["surgical"]),
        "platelet":    (domain_scores["skin"] + domain_scores["mucosal"]) / max(1, domain_max["skin"]+domain_max["mucosal"]),
        "itp":         domain_scores["skin"] / max(1, domain_max["skin"]),
        "haemophilia": domain_scores["deep"] / max(1, domain_max["deep"]),
        "factor":      (domain_scores["deep"] + domain_scores["surgical"]) / max(1, domain_max["deep"]+domain_max["surgical"]),
        "mixed":       sum(domain_scores.values()) / max(1, sum(domain_max.values())),
    }
    vals   = [d_scores_display[d] for d in disorders_show]
    d_cols2 = [DISORDER_STYLE[d]["color"] for d in disorders_show]
    y_pos  = np.arange(len(disorders_show))
    bars3  = ax3.barh(y_pos, vals, color=[c+"55" for c in d_cols2], height=0.55,
                      edgecolor="#0b1220")
    highlight = disorders_show.index(result["disorder"]) if result["disorder"] in disorders_show else -1
    if highlight >= 0:
        ax3.barh(highlight, vals[highlight], color=d_cols2[highlight], height=0.55, edgecolor="#0b1220")
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels([t["disorders"][d] for d in disorders_show], fontsize=7.5)
    ax3.set_xlim(0, 1.2); ax3.set_xticks([])
    ax3.tick_params(left=False, labelsize=7.5)
    for sp in ax3.spines.values(): sp.set_visible(False)
    for lbl in ax3.get_yticklabels(): lbl.set_color("#94a3b8")
    ax3.set_title(t["likely_disorder"], color="#e2e8f0", fontsize=10, pad=8)
    for bar, val, dc in zip(bars3, vals, d_cols2):
        ax3.text(val+0.03, bar.get_y()+bar.get_height()/2,
                 f"{val*100:.0f}%", va="center", fontsize=7, color=dc)

    plt.tight_layout(pad=2.0)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=145, bbox_inches="tight",
                facecolor="#0b1220", edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf


def build_pdf(patient, questions, answers, result, t):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    NAVY  = colors.HexColor("#04080f")
    TEAL  = colors.HexColor("#38bdf8")
    SLATE = colors.HexColor("#111c2e")
    BDR   = colors.HexColor("#1e3050")
    LIGHT = colors.HexColor("#e2e8f0")
    MUTED = colors.HexColor("#64748b")
    RISK  = colors.HexColor(DISORDER_STYLE[result["disorder"]]["color"])
    YES_C = colors.HexColor("#f43f5e")
    NO_C  = colors.HexColor("#34d399")

    def sty(name, **kw): return ParagraphStyle(name, **kw)
    S = {
        "title":  sty("T", fontSize=20, textColor=TEAL, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=3),
        "sub":    sty("S", fontSize=8,  textColor=MUTED, fontName="Helvetica", alignment=TA_CENTER, spaceAfter=10),
        "sect":   sty("Se",fontSize=10, textColor=TEAL, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=5),
        "body":   sty("B", fontSize=8.5,textColor=LIGHT, fontName="Helvetica", leading=13, spaceAfter=3),
        "risk":   sty("R", fontSize=14, textColor=RISK, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4),
        "adv":    sty("A", fontSize=8.5,textColor=LIGHT, fontName="Helvetica-Oblique", leading=13),
        "footer": sty("F", fontSize=7,  textColor=MUTED, fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceBefore=10),
    }

    story = []
    story.append(Paragraph(t["app_title"], S["title"]))
    story.append(Paragraph("ISTH BAT Framework · Bleeding Disorder Classification", S["sub"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8))

    # Patient
    story.append(Paragraph(t["patient_title"], S["sect"]))
    pt = [
        [t["name_label"], patient["name"], t["date_label"], patient["date"]],
        [t["age_label"],  f"{patient['age']} yrs", t["gender_badge"], patient["gender"]],
        [t["id_label"],   patient.get("pid","—"), "", ""],
    ]
    pt_t = Table(pt, colWidths=[3*cm,6*cm,3*cm,5*cm])
    pt_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),SLATE),("GRID",(0,0),(-1,-1),.4,BDR),
        ("TEXTCOLOR",(0,0),(0,-1),MUTED),("TEXTCOLOR",(2,0),(2,-1),MUTED),
        ("TEXTCOLOR",(1,0),(1,-1),LIGHT),("TEXTCOLOR",(3,0),(3,-1),LIGHT),
        ("FONTNAME",(0,0),(0,-1),"Helvetica"),("FONTNAME",(1,0),(1,-1),"Helvetica-Bold"),
        ("FONTNAME",(2,0),(2,-1),"Helvetica"),("FONTNAME",(3,0),(3,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8.5),("PADDING",(0,0),(-1,-1),5),
    ]))
    story.append(pt_t); story.append(Spacer(1,8))

    # Score summary
    story.append(HRFlowable(width="100%", thickness=.4, color=BDR, spaceAfter=6))
    story.append(Paragraph(t["results_title"], S["sect"]))
    yes_c = sum(1 for v in answers.values() if v=="Yes")
    no_c  = sum(1 for v in answers.values() if v=="No")
    sc = [[t["positive"],t["negative"],t["answered"],t["pattern_score"]],
          [str(yes_c), str(no_c), str(len(answers)), str(result["total_yes_weight"])]]
    sc_t = Table(sc, colWidths=["25%","25%","25%","25%"])
    sc_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0e4f6e")),
        ("BACKGROUND",(0,1),(-1,1),SLATE),
        ("TEXTCOLOR",(0,0),(-1,0),LIGHT),("TEXTCOLOR",(0,1),(-1,1),TEAL),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,0),8),("FONTSIZE",(0,1),(-1,1),15),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("PADDING",(0,0),(-1,-1),7),("GRID",(0,0),(-1,-1),.4,BDR),
    ]))
    story.append(sc_t); story.append(Spacer(1,8))

    # Disorder + severity
    story.append(HRFlowable(width="100%", thickness=.4, color=BDR, spaceAfter=6))
    story.append(Paragraph(t["likely_disorder"], S["sect"]))
    dis_label = t["disorders"][result["disorder"]]
    sev_label = t["severities"][result["severity"]]
    story.append(Paragraph(f"{DISORDER_STYLE[result['disorder']]['icon']}  {dis_label}", S["risk"]))
    story.append(Paragraph(f"<b>{t['severity_label']}:</b> {sev_label}", S["body"]))
    story.append(Paragraph(f"<b>{t['workup_label']}:</b> {result['workup']}", S["adv"]))
    story.append(Spacer(1,6))

    # Domain scores
    story.append(HRFlowable(width="100%", thickness=.4, color=BDR, spaceAfter=6))
    story.append(Paragraph(t["domain_breakdown"], S["sect"]))
    dom_data = [[t.get(f"domain_{d}","—"),
                 f"{result['domain_scores'][d]} / {result['domain_max'][d]}"]
                for d in ["mucosal","skin","deep","surgical"]]
    dom_t = Table(dom_data, colWidths=["60%","40%"])
    dom_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),SLATE),("GRID",(0,0),(-1,-1),.4,BDR),
        ("TEXTCOLOR",(0,0),(0,-1),LIGHT),("TEXTCOLOR",(1,0),(1,-1),TEAL),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8.5),
        ("PADDING",(0,0),(-1,-1),5),("ALIGN",(1,0),(1,-1),"RIGHT"),
    ]))
    story.append(dom_t); story.append(Spacer(1,8))

    # Answers
    story.append(HRFlowable(width="100%", thickness=.4, color=BDR, spaceAfter=6))
    story.append(Paragraph(t["answer_summary"], S["sect"]))
    ans_data = [["#","Category","Question","Answer"]]
    for i,q in enumerate(questions):
        a = answers.get(i,"—")
        ans_data.append([str(i+1), q["category"], q["text"],
                         "YES" if a=="Yes" else ("NO" if a=="No" else "—")])
    ans_t = Table(ans_data, colWidths=[.8*cm, 3.5*cm, 11*cm, 1.5*cm])
    ts = TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0e4f6e")),
        ("TEXTCOLOR",(0,0),(-1,0),LIGHT),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,0),7.5),
        ("FONTSIZE",(0,1),(-1,-1),7.5),("PADDING",(0,0),(-1,-1),4),
        ("GRID",(0,0),(-1,-1),.4,BDR),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[SLATE,colors.HexColor("#1a2a40")]),
        ("ALIGN",(0,0),(0,-1),"CENTER"),("ALIGN",(3,0),(3,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ])
    for i,q in enumerate(questions):
        a = answers.get(i,"—")
        row = i+1
        if a=="Yes":  ts.add("TEXTCOLOR",(3,row),(3,row),YES_C); ts.add("FONTNAME",(3,row),(3,row),"Helvetica-Bold")
        elif a=="No": ts.add("TEXTCOLOR",(3,row),(3,row),NO_C)
        else:         ts.add("TEXTCOLOR",(3,row),(3,row),MUTED)
        ts.add("TEXTCOLOR",(1,row),(1,row),colors.HexColor("#818cf8"))
        ts.add("TEXTCOLOR",(2,row),(2,row),LIGHT)
        ts.add("TEXTCOLOR",(0,row),(0,row),MUTED)
    ans_t.setStyle(ts)
    story.append(ans_t)

    story.append(HRFlowable(width="100%", thickness=.4, color=BDR, spaceBefore=10, spaceAfter=5))
    story.append(Paragraph(t["disclaimer"], S["footer"]))
    story.append(Paragraph(f"Generated: {patient['date']}  |  ISTH BAT Bleeding Disorder Classification Tool", S["footer"]))

    doc.build(story)
    buf.seek(0)
    return buf


def go(p): st.session_state.page = p

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
defaults = dict(page=0, answers={}, lang="English", gender=None, questions=[],
                pt_name="", pt_age=0, pt_date=str(datetime.date.today()), pt_id="")
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Language selector ─────────────────────────────────────────────────────────
lang_opts = ["English","Malayalam","Hindi","Tamil"]
_, lc, _ = st.columns([3,2,3])
with lc:
    chosen = st.selectbox(
        TR[st.session_state.lang]["lang_label"],
        lang_opts, index=lang_opts.index(st.session_state.lang),
        key="lang_sel", label_visibility="collapsed"
    )
    if chosen != st.session_state.lang:
        st.session_state.lang = chosen
        st.session_state.page = 0
        st.session_state.answers = {}
        st.session_state.gender = None
        st.rerun()

t    = TR[st.session_state.lang]
lang = st.session_state.lang

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 0 — INTRO
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == 0:
    st.markdown(f"""
    <div class='hero'>
      <span class='hero-icon'>🩸</span>
      <h1 class='hero-title'>{t['app_title']}</h1>
      <p class='hero-sub'>{t['app_sub']}</p>
      <div class='pills'>
        <div class='pill'>🗒️ <b>20</b> {t['pill_q']}</div>
        <div class='pill'>⏱️ <b>3–5</b> {t['pill_min']}</div>
        <div class='pill'>📊 {t['pill_result']}</div>
        <div class='pill'>🏥 ISTH BAT</div>
      </div>
    </div>""", unsafe_allow_html=True)

    _, mc, _ = st.columns([1,5,1])
    with mc:
        st.markdown(f"""
        <div class='card'>
          <div class='info-grid'>
            <div class='info-box'>
              <div class='info-icon'>🎯</div>
              <div class='info-title'>{t['purpose_title']}</div>
              <div class='info-body'>{t['purpose_body']}</div>
            </div>
            <div class='info-box'>
              <div class='info-icon'>📋</div>
              <div class='info-title'>{t['instr_title']}</div>
              <div class='info-body'>{t['instr_body']}</div>
            </div>
            <div class='info-box'>
              <div class='info-icon'>🔬</div>
              <div class='info-title'>{t['score_title']}</div>
              <div class='info-body'>{t['score_body']}</div>
            </div>
            <div class='info-box'>
              <div class='info-icon'>🏥</div>
              <div class='info-title'>{t['outcome_title']}</div>
              <div class='info-body'>{t['outcome_body']}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Domain legend
        st.markdown("""
        <div style='background:#0b1220;border:1px solid #1e3050;border-radius:14px;
             padding:1rem 1.3rem;margin-bottom:1rem;'>
          <div style='font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
               color:#38bdf8;margin-bottom:.7rem;'>BLEEDING PATTERN → DISORDER MAPPING</div>
          <div style='display:grid;grid-template-columns:1fr 1fr;gap:.6rem;'>
        """, unsafe_allow_html=True)
        domain_info = [
            ("💧","#38bdf8","Mucosal","Nosebleed · Gum · GI · Menstrual","→ VWD / Platelet"),
            ("🩹","#818cf8","Skin","Petechiae · Purpura · Bruising","→ ITP / Thrombocytopenia"),
            ("🦴","#f43f5e","Deep Tissue","Joint · Muscle · Brain bleeds","→ Haemophilia / Factor"),
            ("🔧","#f59e0b","Surgical","Post-op · Dental · Wound · Transfusion","→ Mixed / Factor"),
        ]
        for icon, color, name, desc, maps in domain_info:
            st.markdown(f"""
            <div style='background:#111c2e;border:1px solid #1e3050;border-radius:10px;padding:.7rem .9rem;'>
              <div style='font-size:.82rem;font-weight:700;color:{color};margin-bottom:.2rem;'>
                {icon} {name}</div>
              <div style='font-size:.75rem;color:#64748b;line-height:1.5;'>{desc}</div>
              <div style='font-size:.73rem;font-weight:600;color:{color};opacity:.7;margin-top:.2rem;'>{maps}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        if st.button(t["proceed_btn"], use_container_width=True, type="primary"):
            go(1); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — PATIENT INFO
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == 1:
    _, mc, _ = st.columns([1,5,1])
    with mc:
        st.markdown(f"""
        <div class='section-label'>
          <div class='section-icon'>🏥</div>
          <h2 class='section-title'>{t['patient_title']}</h2>
          <p class='section-sub'>{t['patient_sub']}</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        name = st.text_input(t["name_label"], value=st.session_state.pt_name, placeholder=t["name_ph"])
        c1, c2 = st.columns(2)
        with c1: age  = st.number_input(t["age_label"], min_value=0, max_value=120,
                                         value=int(st.session_state.pt_age) if st.session_state.pt_age else 0)
        with c2: date = st.date_input(t["date_label"], value=datetime.date.today())
        pid = st.text_input(t["id_label"], value=st.session_state.pt_id, placeholder=t["id_ph"])
        st.markdown("</div>", unsafe_allow_html=True)

        err = False
        if not name.strip():
            st.markdown(f"<p style='color:#f59e0b;font-size:.85rem;'>{t['name_err']}</p>", unsafe_allow_html=True)
            err = True
        if age < 1 or age > 120:
            st.markdown(f"<p style='color:#f59e0b;font-size:.85rem;'>{t['age_err']}</p>", unsafe_allow_html=True)
            err = True

        b1, b2 = st.columns(2)
        with b1:
            if st.button(t["back_btn"], use_container_width=True): go(0); st.rerun()
        with b2:
            if st.button(t["gender_next"], use_container_width=True, type="primary"):
                if not err:
                    st.session_state.pt_name = name.strip()
                    st.session_state.pt_age  = age
                    st.session_state.pt_date = str(date)
                    st.session_state.pt_id   = pid.strip()
                    go(2); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — GENDER
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == 2:
    _, mc, _ = st.columns([1,4,1])
    with mc:
        st.markdown(f"""
        <div class='section-label'>
          <div class='section-icon'>⚧</div>
          <h2 class='section-title'>{t['gender_title']}</h2>
          <p class='section-sub'>{t['gender_sub']}</p>
        </div>""", unsafe_allow_html=True)

        opts   = [t["male"], t["female"], t["other"]]
        icons  = ["♂","♀","⚧"]
        colors_g = ["#38bdf8","#f472b6","#a78bfa"]
        descs  = [t["male_desc"], t["female_desc"], t["other_desc"]]

        for i, (opt, icon, color, desc) in enumerate(zip(opts, icons, colors_g, descs)):
            st.markdown(f"""
            <div class='gender-card'>
              <div class='gender-icon' style='filter:drop-shadow(0 0 8px {color}88);color:{color};'>{icon}</div>
              <div>
                <div class='gender-name' style='color:{color};'>{opt}</div>
                <div class='gender-desc'>{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(opt, use_container_width=True, key=f"g_{i}"):
                st.session_state.gender    = opt
                st.session_state.answers   = {}
                st.session_state.questions = get_questions(lang, opt)
                go(3); st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t["back_btn"], use_container_width=True): go(1); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGES 3..N+2 — QUESTIONS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page >= 3:
    questions   = st.session_state.questions
    total       = len(questions)
    result_page = total + 3

    # ── Question pages ────────────────────────────────────────────────────────
    if st.session_state.page < result_page:
        q_idx = st.session_state.page - 3
        if q_idx >= total: go(result_page); st.rerun()
        q = questions[q_idx]
        domain_key = q["domain"]
        domain_name = t.get(f"domain_{domain_key}", domain_key)
        d_color = DOMAIN_COLOR[domain_key]
        d_icon  = DOMAIN_ICON[domain_key]

        # Progress
        st.markdown(f"""
        <div class='step-row'>
          <span class='step-left'>{t['isth_label'] if 'isth_label' in t else 'Screening'} &nbsp;·&nbsp;
            <span style='color:#a78bfa;font-size:.76rem;'>{st.session_state.gender or ""}</span></span>
          <span class='step-right'>{t['q_label']} {q_idx+1} {t['of_label']} {total}</span>
        </div>""", unsafe_allow_html=True) if 'isth_label' in t else None

        st.markdown(f"""
        <div class='step-row'>
          <span class='step-left'>Bleeding Disorder Screening &nbsp;·&nbsp;
            <span style='color:#a78bfa;font-size:.76rem;'>{st.session_state.gender or ""}</span></span>
          <span class='step-right'>{t['q_label']} {q_idx+1} {t['of_label']} {total}</span>
        </div>""", unsafe_allow_html=True)
        st.progress(q_idx / total)
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        # Patient strip
        st.markdown(f"""
        <div class='pt-strip'>
          <span class='pt-item'>👤 <strong>{st.session_state.pt_name}</strong></span>
          <span class='pt-item'>{t['age_label']}: <strong>{st.session_state.pt_age}</strong></span>
          <span class='pt-item'>{t['date_label']}: <strong>{st.session_state.pt_date}</strong></span>
        </div>""", unsafe_allow_html=True)

        _, mc, _ = st.columns([1,6,1])
        with mc:
            st.markdown(f"""
            <div class='card'>
              <div class='q-domain' style='color:{d_color}!important;border-color:{d_color}44;'>
                {d_icon} {domain_name}
              </div>
              <div class='q-text'>{q['text']}</div>
              <hr class='divider'>
              <div class='q-hint'>🔬 &nbsp;{q['hint']}</div>
            </div>""", unsafe_allow_html=True)

            prev = st.session_state.answers.get(q_idx)
            c1, c2 = st.columns(2)
            with c1:
                lbl = (t["yes_btn"]+" ✓") if prev=="Yes" else t["yes_btn"]
                if st.button(lbl, use_container_width=True,
                             type="primary" if prev=="Yes" else "secondary",
                             key=f"y_{q_idx}"):
                    st.session_state.answers[q_idx] = "Yes"
                    go(st.session_state.page+1); st.rerun()
            with c2:
                lbl = (t["no_btn"]+" ✓") if prev=="No" else t["no_btn"]
                if st.button(lbl, use_container_width=True,
                             type="primary" if prev=="No" else "secondary",
                             key=f"n_{q_idx}"):
                    st.session_state.answers[q_idx] = "No"
                    go(st.session_state.page+1); st.rerun()

            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            nb1, nb2, nb3 = st.columns([2,3,2])
            with nb1:
                if st.session_state.page > 3:
                    if st.button(t["back_btn"], use_container_width=True):
                        go(st.session_state.page-1); st.rerun()
            with nb3:
                if q_idx in st.session_state.answers:
                    if st.button(t["skip_btn"], use_container_width=True):
                        go(st.session_state.page+1); st.rerun()

            # Dot navigator
            dots = "<div class='dots'>"
            for i in range(total):
                a = st.session_state.answers.get(i)
                c = d_color if i==q_idx else ("#f43f5e" if a=="Yes" else ("#34d399" if a=="No" else "#1e3050"))
                dots += f"<div class='dot' style='background:{c};'></div>"
            dots += "</div>"
            st.markdown(dots, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  RESULTS PAGE
    # ══════════════════════════════════════════════════════════════════════════
    else:
        questions = st.session_state.questions
        answers   = st.session_state.answers
        result    = classify(questions, answers, t)
        yes_c     = sum(1 for v in answers.values() if v=="Yes")
        no_c      = sum(1 for v in answers.values() if v=="No")
        dis       = result["disorder"]
        sev       = result["severity"]
        ds        = DISORDER_STYLE[dis]
        sev_color = SEVERITY_COLOR[sev]
        patient   = dict(name=st.session_state.pt_name, age=st.session_state.pt_age,
                         date=st.session_state.pt_date, pid=st.session_state.pt_id,
                         gender=st.session_state.gender or "—")

        st.markdown(f"""
        <div class='section-label'>
          <div class='section-icon'>📊</div>
          <h2 class='section-title'>{t['results_title']}</h2>
          <p class='section-sub'>{t['results_sub']}</p>
        </div>""", unsafe_allow_html=True)

        # Patient strip
        st.markdown(f"""
        <div class='pt-strip' style='border-radius:12px;padding:.7rem 1.3rem;margin-bottom:.9rem;'>
          <span class='pt-item'>👤 <strong>{patient['name']}</strong></span>
          <span class='pt-item'>🎂 <strong>{patient['age']} yrs</strong></span>
          <span class='pt-item'>📅 <strong>{patient['date']}</strong></span>
          <span class='pt-item'>{t['gender_badge']}: <strong style='color:#a78bfa;'>{patient['gender']}</strong></span>
          {f'<span class="pt-item">ID: <strong>{patient["pid"]}</strong></span>' if patient.get("pid") else ""}
        </div>""", unsafe_allow_html=True)

        _, mc, _ = st.columns([1,6,1])
        with mc:
            # Stats bar
            st.markdown(f"""
            <div class='stat-row'>
              <div class='stat-item'>
                <div class='stat-val' style='color:{ds["color"]};'>{yes_c}</div>
                <div class='stat-lbl'>{t['positive']}</div>
              </div>
              <div class='stat-item'>
                <div class='stat-val' style='color:#34d399;'>{no_c}</div>
                <div class='stat-lbl'>{t['negative']}</div>
              </div>
              <div class='stat-item'>
                <div class='stat-val' style='color:#38bdf8;'>{len(answers)}</div>
                <div class='stat-lbl'>{t['answered']}</div>
              </div>
              <div class='stat-item'>
                <div class='stat-val' style='color:{ds["color"]};'>{result['total_yes_weight']}</div>
                <div class='stat-lbl'>{t['pattern_score']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            # ── Main result card ──────────────────────────────────────────────
            st.markdown(f"""
            <div class='result-card' style='background:{ds["bg"]};border-color:{ds["border"]};'>
              <div style='font-size:2.8rem;margin-bottom:.3rem;'>{ds["icon"]}</div>
              <div style='font-size:.75rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
                   color:{ds["color"]};opacity:.7;margin-bottom:.1rem;'>{t['likely_disorder']}</div>
              <div class='disorder-name' style='color:{ds["color"]};'>{t['disorders'][dis]}</div>
              <div class='severity-pill' style='background:{sev_color}22;color:{sev_color};
                   border:1px solid {sev_color}55;'>
                🎚️ &nbsp; {t['severity_label']}: {t['severities'][sev]}
              </div>
              <div class='workup-label'>{t['workup_label']}</div>
              <div class='workup-box'>{result['workup']}</div>
              <div style='margin-top:.9rem;font-size:.86rem;color:#94a3b8;line-height:1.6;'>
                {result['advice']}
              </div>
            </div>""", unsafe_allow_html=True)

            # ── Domain breakdown ──────────────────────────────────────────────
            st.markdown(f"#### 🧩 {t['domain_breakdown']}")
            dom_rows = ""
            for d in ["mucosal","skin","deep","surgical"]:
                sc  = result["domain_scores"][d]
                mx  = max(result["domain_max"][d], 1)
                pct = sc / mx
                dc  = DOMAIN_COLOR[d]
                di  = DOMAIN_ICON[d]
                dn  = t.get(f"domain_{d}", d)
                dom_rows += f"""
                <div class='domain-row'>
                  <div class='domain-name'>{di} {dn}</div>
                  <div class='domain-bar-bg'>
                    <div class='domain-bar-fill' style='width:{pct*100:.0f}%;background:{dc};'></div>
                  </div>
                  <div class='domain-score'>{sc}/{mx}</div>
                </div>"""
            st.markdown(f"<div class='card' style='padding:1rem 1.4rem;'>{dom_rows}</div>",
                        unsafe_allow_html=True)

            # ── Chart ────────────────────────────────────────────────────────
            st.markdown("#### 📈 Pattern Analysis Chart")
            chart_buf = make_chart(questions, answers, result["domain_scores"],
                                   result["domain_max"], result, t)
            st.image(chart_buf, use_container_width=True)
            chart_buf.seek(0)

            # ── Active domains ────────────────────────────────────────────────
            active_doms = [d for d in ["mucosal","skin","deep","surgical"]
                           if result["domain_scores"][d] > 0]
            if active_doms:
                st.markdown(f"#### {t['active_domains']}")
                tags = ""
                for d in active_doms:
                    dc = DOMAIN_COLOR[d]
                    dn = t.get(f"domain_{d}", d)
                    di = DOMAIN_ICON[d]
                    sc = result["domain_scores"][d]
                    mx = result["domain_max"][d]
                    tags += f"""<span style='background:{dc}18;border:1px solid {dc}44;color:{dc};
                         border-radius:99px;padding:.3rem .9rem;margin:.2rem;display:inline-flex;
                         align-items:center;gap:.4rem;font-size:.83rem;font-weight:600;'>
                         {di} {dn} &nbsp;
                         <span style='font-size:.75rem;opacity:.7;'>{sc}/{mx}</span></span>"""
                st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:1rem;'>{tags}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style='background:#022c22;border:1px solid #34d39944;
                    border-radius:12px;padding:.9rem 1.2rem;color:#34d399;
                    font-size:.9rem;margin-bottom:1rem;'>{t['no_symptoms']}</div>""",
                    unsafe_allow_html=True)

            # ── Answer summary ────────────────────────────────────────────────
            st.markdown(f"#### {t['answer_summary']}")
            rows = ""
            for i, q in enumerate(questions):
                a   = answers.get(i, "—")
                ac  = "#f43f5e" if a=="Yes" else ("#34d399" if a=="No" else "#64748b")
                dc  = DOMAIN_COLOR[q["domain"]]
                rows += f"""
                <div class='answer-row'>
                  <span class='ans-num'>Q{i+1}</span>
                  <span class='ans-cat' style='color:{dc};'>{q['category']}</span>
                  <span class='ans-text'>{q['text']}</span>
                  <span class='ans-val' style='color:{ac};background:{ac}18;
                       border-radius:6px;padding:.1rem .45rem;'>{a}</span>
                </div>"""
            st.markdown(f"<div class='card' style='padding:1.1rem 1.4rem;'>{rows}</div>",
                        unsafe_allow_html=True)

            # ── Disclaimer ────────────────────────────────────────────────────
            st.markdown(f"<div class='disclaimer-box'>{t['disclaimer']}</div>",
                        unsafe_allow_html=True)
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

            # ── PDF download ──────────────────────────────────────────────────
            with st.spinner(t["pdf_gen"]):
                chart_buf.seek(0)
                pdf_buf = build_pdf(patient, questions, answers, result, t)
            safe = (patient["name"] or "patient").replace(" ","_")
            st.download_button(
                label=t["pdf_btn"],
                data=pdf_buf,
                file_name=f"BleedingDisorder_{safe}_{patient['date']}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )

            st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.button(t["retake_btn"], use_container_width=True, type="primary"):
                    for k in ["answers","gender","questions","pt_name","pt_id"]:
                        st.session_state[k] = {} if k=="answers" else ([] if k=="questions" else (None if k=="gender" else ""))
                    st.session_state.pt_age = 0
                    go(0); st.rerun()
            with b2:
                if st.button(t["review_btn"], use_container_width=True):
                    go(3); st.rerun()

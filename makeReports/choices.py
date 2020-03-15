"""
Holds static choice tuples that should not change
"""
BLOOMS_CHOICES = (
    ('', '------'),
    ("KN","Knowledge"),
    ("CO","Comprehension"),
    ("AP", "Application"),
    ("AN", "Analysis"),
    ("SN","Synthesis"),
    ("EV", "Evaluation"))
RUBRIC_GRADES_CHOICES = (
    ("DNM","Does Not Meet/Did Not Include"),
    ("MC", "Meets with Concerns"),
    ("ME", "Meets Established"))
LEVELS = (
    ("UG", "Undergraduate"),
    ("GR", "Graduate"))
SECTIONS = (
    (1,"I. Student Learning Outcomes"),
    (2,"II. Assessment Methods"),
    (3,"III. Data Collection and Analysis"),
    (4,"IV. Decisions and Actions"))
DOMAIN_CHOICES = (
    ("E", "Examination"),
    ("P","Product"),
    ("F","Performance"))
#To prevent breaking filtering, met, partially met, not met, and unknown should maintain their positions
#However, changing the display name does not matter
SLO_STATUS_CHOICES = (
    ("Met", "Met"), 
    ("Partially Met", "Partially Met"), 
    ("Not Met", "Not Met"), 
    ("Unknown", "Unknown"))
FREQUENCY_CHOICES = (
    ("S","Once/semester"),
    ("Y","Once/year"),
    ("O","Other")    
)

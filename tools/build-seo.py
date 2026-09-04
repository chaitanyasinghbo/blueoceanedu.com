#!/usr/bin/env python3
"""Write the search and answer-engine block into every page's head.

    python3 tools/build-seo.py
    python3 tools/build-seo.py --check    # exit 1 if a rebuild is pending

The block sits between `<!-- @seo -->` and `<!-- /@seo -->` in each `<head>`,
the same way analytics sits between the `@analytics` sentinels, and it carries
the title, the description, the canonical, the robots directive, Open Graph,
the Twitter card, and one `application/ld+json` graph.

**Why this is generated rather than written.** The organisation and the founder
are the two entities the whole site is trying to make legible, and both have to
be described identically on every page or a search engine reads them as several
similar entities rather than one. Kept by hand across eight pages that is a
promise; kept here it is a fact. It is the same argument
`tools/build-landing-pages.py` makes about the hero.

Three rules govern what may go in a node, and none of them is negotiable.

**Every claim in the schema is visible on the page.** A `Person` node that
outruns its own page is what an audit flags, and an `Organization` claiming
hours or a price the site never shows is the same failure. When a claim is
worth making, put it on the page first and in the schema second.

**Every URL in `sameAs` resolves and belongs to us.** This is not pedantry
here, it is the whole problem. There are at least four unrelated education
businesses trading as some form of *Blue Ocean*, and one of them, a Vietnamese
study-abroad agency, holds `linkedin.com/company/blue-ocean-education` and
`youtube.com/@blueoceaneducation`. Adding either to `sameAs` would tell Google
in machine-readable terms that we are them. `edjustice.in` and `sanjaykumar.in`
are dead and stay out for the ordinary reason.

**URLs have no `.html`.** Cloudflare Pages answers `/founder.html` with a 308
to `/founder`, so the extensionless form is what the site serves and what every
canonical, `og:url`, `@id` and sitemap entry states. The links in the markup
are still written `founder.html`; a 308 is followed and consolidated, and
rewriting several hundred hrefs to gain nothing is not worth the risk of
breaking one. The canonical is what decides which URL is indexed.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://blueoceanedu.com"

OPEN = "<!-- @seo -->"
CLOSE = "<!-- /@seo -->"

ORG = ORIGIN + "/#organisation"
PERSON = ORIGIN + "/#sanjay-kumar"
SITE = ORIGIN + "/#website"
BOOK = ORIGIN + "/#katihar-to-kennedy"

OG_CARD = ORIGIN + "/og-card.jpg"
OG_CARD_ALT = ("The Great Dome at MIT, the campus picture Blue Ocean "
               "Education's home page opens on")
COMMENCEMENT = ORIGIN + "/founder/commencement.jpg"


# ── The two nodes the whole site exists to make legible ──────────────

def organisation(with_catalog=False):
    """Blue Ocean Education Consulting.

    Typed as both an `EducationalOrganization` and a `ProfessionalService`.
    The first is what the business is; the second is a `LocalBusiness`
    subtype, which is what makes an address in Connaught Place mean something
    to a search engine answering "admissions consultant near me" rather than
    reading as decoration under a national brand.

    `disambiguatingDescription` is doing real work and is not filler. Searching
    the name returns a supply-chain training institute in Kerala, an IT
    consultancy in Bangalore, a recruitment LLP, and a Vietnamese study-abroad
    agency, all trading as Blue Ocean something. The property exists for
    exactly this, and the same statement is on `fit.html` in the FAQ so the
    claim is visible where the schema makes it.
    """
    node = {
        "@type": ["EducationalOrganization", "ProfessionalService"],
        "@id": ORG,
        "name": "Blue Ocean Education Consulting",
        "legalName": "Blue Ocean Education Consulting",
        "alternateName": [
            "Blue Ocean Education",
            "Blue Ocean Education Consulting India",
            "Blue Ocean Admissions",
        ],
        "url": ORIGIN + "/",
        "logo": {
            "@type": "ImageObject",
            "@id": ORIGIN + "/#logo",
            "url": ORIGIN + "/brand/logo-lockup.svg",
            "contentUrl": ORIGIN + "/brand/logo-lockup.svg",
            "caption": "Blue Ocean Education Consulting",
        },
        "image": {"@id": ORIGIN + "/#logo"},
        "slogan": "Develop the student. Admissions follow.",
        "description": (
            "Blue Ocean Education Consulting is a founder-led admissions "
            "advisory in New Delhi. It helps hardworking Indian students in "
            "grades 8 to 12 build the depth, originality and discipline "
            "required to compete for admission to Harvard, Yale, Oxford, "
            "Cambridge and the world's most selective universities, and "
            "advises graduate applicants to elite MBA and Masters programmes."
        ),
        "disambiguatingDescription": (
            "Blue Ocean Education Consulting is the New Delhi undergraduate "
            "and graduate admissions advisory founded by Dr. Sanjay Kumar, "
            "PhD, a Harvard Kennedy School MPA and former India Country "
            "Director of Harvard's Lakshmi Mittal and Family South Asia "
            "Institute. It is a separate and unaffiliated business from Blue "
            "Ocean Academy, Blue Ocean Learning, Blue Ocean Corporation and "
            "every other organisation trading under a similar name."
        ),
        "founder": {"@id": PERSON},
        "employee": {"@id": PERSON},
        "telephone": "+91-98211-18128",
        "email": "admissions@blueoceanedu.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "6, School Lane, Connaught Place",
            "addressLocality": "New Delhi",
            "addressRegion": "Delhi",
            "postalCode": "110001",
            "addressCountry": "IN",
        },
        # Mon to Sat, 10am to 7pm IST, as stated in the footer of every page.
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday"],
            "opens": "10:00",
            "closes": "19:00",
        }],
        "areaServed": [
            {"@type": "Country", "name": "India"},
            {"@type": "City", "name": "New Delhi"},
            {"@type": "City", "name": "Gurugram"},
            {"@type": "City", "name": "Noida"},
            {"@type": "City", "name": "Mumbai"},
            {"@type": "City", "name": "Pune"},
            {"@type": "City", "name": "Bengaluru"},
        ],
        "knowsAbout": [
            "Undergraduate admissions to universities in the United States",
            "Undergraduate admissions to the United Kingdom and UCAS",
            "Ivy League admissions for Indian students",
            "Oxford and Cambridge admissions for Indian students",
            "Common Application essays and supplemental essays",
            "Student profile development and the admissions spike",
            "Research mentorship and publication for school students",
            "Olympiads, competitions and selective summer programmes",
            "SAT and ACT strategy, and Advanced Placement course choice",
            "IB Diploma, IGCSE, A Level, CBSE and ICSE subject selection",
            "Merit scholarships and financial aid for international students",
            "MBA and Masters admissions to Harvard, Wharton, INSEAD and LBS",
        ],
        "audience": {
            "@type": "EducationalAudience",
            "audienceType": (
                "Students in grades 8 to 12 in India applying to universities "
                "abroad, their parents, and graduate applicants to MBA and "
                "Masters programmes"
            ),
        },
        # One entry, and it is the one profile that is verifiably ours. Every
        # other Blue Ocean handle found while writing this belonged to an
        # unrelated company. See the module docstring.
        "sameAs": ["https://www.instagram.com/blueocean.education/"],
    }
    if with_catalog:
        node["hasOfferCatalog"] = offer_catalog()
    return node


def offer_catalog():
    """The four service tracks, named on index.html and nowhere else.

    Carried on the home page's graph only, because that is the one page that
    lists them. A catalog repeated on a page that does not show it is the
    claim-outruns-the-page failure the docstring warns about.
    """
    tracks = [
        ("Early Architecture",
         "Grades 8 to 10",
         "Profile building from the ground up. Subject combinations, the first "
         "genuine extracurricular commitments, and the foundations laid before "
         "the application race begins."),
        ("Strategic Build",
         "Grade 11",
         "The critical year. University list, narrative positioning, essay "
         "ideation, recommender relationships, and test strategy chosen on "
         "diagnostic evidence."),
        ("Final Year Admissions",
         "Grade 12",
         "Full-cycle application support across the Common Application and "
         "UCAS. Personal statement and supplements, interviews, waitlist and "
         "deferral strategy, financial aid, and decision day."),
        ("Masters and MBA Admissions",
         "Graduate",
         "Advisory for postgraduate applicants to MBA, MPA and MPP, LLM and "
         "specialised Masters programmes."),
    ]
    return {
        "@type": "OfferCatalog",
        "name": "Blue Ocean Education programmes",
        "itemListElement": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": name,
                    "serviceType": "University admissions advisory",
                    "description": desc,
                    "audience": {"@type": "EducationalAudience",
                                 "educationalRole": "student",
                                 "audienceType": band},
                    "provider": {"@id": ORG},
                    "areaServed": {"@type": "Country", "name": "India"},
                },
            }
            for name, band, desc in tracks
        ],
    }


def person():
    """Dr. Sanjay Kumar.

    Repeated in full on every page rather than referenced by `@id` alone. He is
    the answer to a large share of the queries this site needs to win, and a
    bare `@id` reference only resolves for a crawler that has already fetched
    the page holding the definition. Repetition is a few hundred bytes; a
    half-defined person is an entity that never consolidates.

    `disambiguatingDescription` again earns its place. Wikipedia carries a
    Sanjay Kumar who is a psephologist and former director of CSDS, and another
    who is a Delhi housing activist, and the name is common enough that an
    answer engine will happily merge all three.
    """
    return {
        "@type": "Person",
        "@id": PERSON,
        "name": "Sanjay Kumar",
        "alternateName": ["Dr. Sanjay Kumar", "Sanjay Kumar, PhD"],
        "honorificPrefix": "Dr.",
        "honorificSuffix": "PhD",
        "gender": "Male",
        "jobTitle": "Founder",
        "description": (
            "Dr. Sanjay Kumar is the founder of Blue Ocean Education "
            "Consulting, an admissions advisory in New Delhi. He grew up in "
            "Katihar, Bihar, studied political science at Delhi University and "
            "Jawaharlal Nehru University, and took an MPA at Harvard Kennedy "
            "School in 2015 on a full scholarship as a Ford Foundation Mason "
            "Fellow. He then ran Harvard's work in India as India Country "
            "Director of the Lakshmi Mittal and Family South Asia Institute, "
            "and served as President of the Harvard Club of India. He works "
            "directly with every student Blue Ocean takes on."
        ),
        "disambiguatingDescription": (
            "The Dr. Sanjay Kumar who founded Blue Ocean Education Consulting "
            "in New Delhi and wrote Katihar to Kennedy. He is a Harvard "
            "Kennedy School MPA and the former India Country Director of "
            "Harvard's Mittal South Asia Institute, and is a different person "
            "from the psephologist and CSDS director of the same name and from "
            "the Delhi housing rights activist of the same name."
        ),
        "url": ORIGIN + "/founder",
        "mainEntityOfPage": {"@id": ORIGIN + "/founder#webpage"},
        "image": {
            "@type": "ImageObject",
            "url": COMMENCEMENT,
            "width": 900,
            "height": 1350,
            "caption": "Dr. Sanjay Kumar at Harvard commencement",
        },
        "nationality": {"@type": "Country", "name": "India"},
        "birthPlace": {
            "@type": "Place",
            "name": "Katihar, Bihar, India",
            "address": {"@type": "PostalAddress", "addressLocality": "Katihar",
                        "addressRegion": "Bihar", "addressCountry": "IN"},
        },
        "worksFor": {"@id": ORG},
        "founderOf": {"@id": ORG},
        "workLocation": {
            "@type": "Place",
            "address": {"@type": "PostalAddress",
                        "streetAddress": "6, School Lane, Connaught Place",
                        "addressLocality": "New Delhi", "postalCode": "110001",
                        "addressCountry": "IN"},
        },
        "alumniOf": [
            {"@type": "CollegeOrUniversity",
             "name": "Harvard Kennedy School, Harvard University",
             "url": "https://www.hks.harvard.edu/"},
            {"@type": "CollegeOrUniversity",
             "name": "Jawaharlal Nehru University",
             "url": "https://www.jnu.ac.in/"},
            {"@type": "CollegeOrUniversity", "name": "University of Delhi",
             "url": "https://www.du.ac.in/"},
            {"@type": "CollegeOrUniversity",
             "name": "Institute of Social Studies, The Hague",
             "url": "https://www.iss.nl/en"},
        ],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential",
             "credentialCategory": "degree",
             "name": "Master in Public Administration, Harvard Kennedy School",
             "dateCreated": "2015"},
            {"@type": "EducationalOccupationalCredential",
             "credentialCategory": "degree",
             "name": "PhD, Jawaharlal Nehru University",
             "dateCreated": "2002"},
        ],
        "award": "Ford Foundation Mason Fellowship, Harvard Kennedy School, 2014-15",
        "knowsAbout": [
            "Undergraduate admissions to universities in the United States "
            "and the United Kingdom",
            "Student profile development",
            "Research mentorship for school students",
            "Admissions essays and applications",
            "Education policy",
            "Public policy",
        ],
        "knowsLanguage": ["English", "Hindi"],
        "sameAs": [
            "https://www.linkedin.com/in/sanjay-kumar-phd-61142579/",
            "https://mittalsouthasiainstitute.harvard.edu/2016/12/sai-welcomes-sanjay-kumar-india-country-director/",
            "https://www.hks.harvard.edu/faculty-research/library-research-services/collections/community-voices-perspectives/katihar",
            "https://hr.economictimes.indiatimes.com/news/industry/upgrad-appoints-dr-sanjay-kumar-as-president-corporate-affairs-and-public-policy/88994938",
            "https://timesofindia.indiatimes.com/times-litfest-2019/speakers/sanjay-kumar/articleshow/72143713.cms",
            "https://www.niti.gov.in/sites/default/files/2023-02/HarvardJournal010722_0.pdf",
            "https://www.amazon.com/Katihar-Kennedy-Road-Less-Travelled/dp/B07QC5PZNY",
        ],
    }


def website():
    return {
        "@type": "WebSite",
        "@id": SITE,
        "url": ORIGIN + "/",
        "name": "Blue Ocean Education",
        "alternateName": "Blue Ocean Education Consulting",
        "description": (
            "The site of Blue Ocean Education Consulting, a founder-led "
            "admissions advisory in New Delhi."
        ),
        "inLanguage": "en-IN",
        "publisher": {"@id": ORG},
        "copyrightHolder": {"@id": ORG},
    }


def book():
    return {
        "@type": "Book",
        "@id": BOOK,
        "name": "Katihar to Kennedy: The Road Less Travelled",
        "author": {"@id": PERSON},
        "datePublished": "2019",
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": "Vani Book Company"},
        "url": "https://www.amazon.com/Katihar-Kennedy-Road-Less-Travelled/dp/B07QC5PZNY",
        "sameAs": "https://www.hks.harvard.edu/faculty-research/library-research-services/collections/community-voices-perspectives/katihar",
        "about": ("An account of the road from Katihar, a small town in "
                  "northeast Bihar, to Harvard Kennedy School."),
    }


# ── The FAQ, which is markup on fit.html and a node here ─────────────
#
# The pairs live in this file and `tools/build-faq.py` writes the visible
# markup from the same list, so the answer a family reads and the answer an
# answer engine quotes cannot drift apart. Both are generated from here.
#
# What each question is for is worth stating, because an FAQ written to fill a
# section is worthless and this one is not that. Questions 1, 2 and 3 are the
# brand and founder queries the site currently loses to four unrelated
# companies and two unrelated men. Questions 4 to 8 are the ones a parent
# actually types before a first call, phrased the way they type them.

FAQ = [
    ("What is Blue Ocean Education?",
     "Blue Ocean Education Consulting is a founder-led admissions advisory "
     "based at 6 School Lane, Connaught Place, New Delhi. It works with "
     "hardworking Indian students in grades 8 to 12 who are aiming at Harvard, "
     "Yale, Oxford, Cambridge and the world's most selective universities, and "
     "with graduate applicants to elite MBA and Masters programmes. The work "
     "is student development first: diagnosis, foundations, distinction, "
     "presentation, and the management that holds all four together. "
     "Admissions are the result of that, not the starting point."),

    ("Is Blue Ocean Education the same as Blue Ocean Academy, Blue Ocean "
     "Learning or Blue Ocean Corporation?",
     "No. None of them are connected to us. Blue Ocean Education Consulting is "
     "the New Delhi admissions advisory founded by Dr. Sanjay Kumar, PhD, and "
     "its only website is blueoceanedu.com. Several unrelated businesses "
     "trade under a similar name, including a supply chain training institute, "
     "an IT consultancy, a recruitment firm, and a study-abroad agency in "
     "Vietnam. If you reached a Blue Ocean that is not at blueoceanedu.com, "
     "it is not us."),

    ("Who is Dr. Sanjay Kumar of Blue Ocean Education?",
     "Dr. Sanjay Kumar, PhD, is the founder of Blue Ocean Education "
     "Consulting. He grew up in Katihar, Bihar, studied political science at "
     "Delhi University and Jawaharlal Nehru University, and took a Master in "
     "Public Administration at Harvard Kennedy School in 2015 on a full "
     "scholarship as a Ford Foundation Mason Fellow. He went on to run "
     "Harvard's work in India as India Country Director of the Lakshmi Mittal "
     "and Family South Asia Institute, and served as President of the Harvard "
     "Club of India. He wrote Katihar to Kennedy, which is held in the Harvard "
     "Kennedy School library collection. He is not the psephologist or the "
     "housing activist who share the name. He reads every diagnosis before it "
     "is signed off and gives every student monthly strategic direction."),

    ("Which universities have Blue Ocean students been admitted to?",
     "More than 100 acceptances at Ivy League and Oxbridge universities across "
     "three admissions cycles, including Harvard, Yale, Columbia, Princeton, "
     "Brown, Cornell, MIT, Stanford, Johns Hopkins, UPenn, Oxford and "
     "Cambridge. Blue Ocean students are admitted at roughly six times the "
     "general applicant rate at Ivy League and US top-15 universities, 96 per "
     "cent are accepted somewhere in the US top 30, and four in five get into "
     "one of their top five choices. The per-university comparison against "
     "each institution's own published rate is on the results page."),

    ("How much does Blue Ocean Education cost?",
     "One annual fee covers everything in the programme: mentorship, "
     "evaluation, projects, workshops, essays, applications and every check-in "
     "between. It follows the April to March academic year and scales with the "
     "length of the programme, so a student joining in grade 8 pays less each "
     "year than one joining in grade 12. The exact figures are shared on the "
     "strategy call, once we know what the student actually needs, and they "
     "are deliberately not published on this site."),

    ("How do you join Blue Ocean Education?",
     "Three steps. A diagnostic call with the family, which settles two "
     "questions: whether we would be the best team for this student, and "
     "whether the student can handle our rigour. Then a short essay from the "
     "student, read for seriousness and curiosity rather than polish. Then a "
     "strategy call, where we walk through exactly how we would help. If we "
     "are not the right fit we say so plainly. You can book the diagnostic "
     "call from the consultation page."),

    ("What grades do you work with, and is it too late to start in grade 11 "
     "or 12?",
     "Grades 8 to 12, and separately with graduate applicants. It is not too "
     "late in grade 11 or grade 12, and the work is different: the Strategic "
     "Build track in grade 11 concentrates on the university list, narrative "
     "positioning, essay ideation, recommender relationships and test "
     "strategy, and the Final Year track in grade 12 is full-cycle "
     "application support across the Common Application and UCAS. Starting "
     "earlier buys room to build depth rather than to package it, which is why "
     "a five-year student pays less per year than a one-year student."),

    ("Which cities does Blue Ocean Education work in?",
     "The office is in Connaught Place, New Delhi, and students are taken on "
     "from Delhi, Gurugram, Noida, Mumbai, Pune and Bengaluru, as well as from "
     "other cities in India and from Indian families living abroad. Weekly "
     "sessions run online, which is what makes the city the student is in "
     "matter less than the work they are willing to do."),

    ("Does Blue Ocean Education guarantee admission?",
     "No, and any consultancy that does is not telling you the truth. No one "
     "controls an admissions committee. What is promised is the work, the "
     "process and the care, and a genuinely limited intake so that every plan "
     "is built around one student. The results published on this site came "
     "from exactly that."),

    ("What boards do you work with, IB, IGCSE, CBSE or ICSE?",
     "All of them, and A Levels and AP as well. Board choice is part of the "
     "Foundations layer rather than a constraint on it: subject combinations "
     "are chosen against the intended major, and where a subject resists, "
     "learning support is arranged. The IB Diploma has its own considerations "
     "for university applications abroad, and the work is adjusted for them."),
]


def faq_node(url):
    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in FAQ
        ],
    }


# ── Per-page configuration ──────────────────────────────────────────
#
# `extra` names graph nodes beyond the four every page carries (page,
# breadcrumb, website, organisation, person).

PAGES = [
    {
        "file": "index.html",
        "path": "/",
        "crumb": None,
        "title": "Blue Ocean Education | Admissions Consultants, New Delhi",
        "description":
            "Founder-led admissions consultants in New Delhi for Indian "
            "students in grades 8 to 12. Over 100 Ivy League and Oxbridge "
            "acceptances, at six times the general admit rate.",
        "page_type": "WebPage",
        "og_type": "website",
        "catalog": True,
    },
    {
        "file": "method.html",
        "path": "/method",
        "crumb": "Method",
        "title": "The Method | Blue Ocean Education",
        "description":
            "How Blue Ocean builds an admissions profile. Diagnosis, "
            "foundations, distinction, presentation, and the management that "
            "holds them together.",
        "page_type": "WebPage",
        "og_type": "article",
    },
    {
        "file": "results.html",
        "path": "/results",
        "crumb": "Results",
        "title": "Results and Admits | Blue Ocean Education",
        "description":
            "Blue Ocean students are admitted at six times the general rate "
            "at Ivy League and US top-15 universities. Rs 1 crore average "
            "scholarship per student.",
        "page_type": "CollectionPage",
        "og_type": "article",
    },
    {
        "file": "founder.html",
        "path": "/founder",
        "crumb": "Founder",
        "title": "Dr. Sanjay Kumar, PhD | Founder, Blue Ocean Education",
        "description":
            "Dr. Sanjay Kumar, PhD, founder of Blue Ocean Education. Harvard "
            "Kennedy School MPA, former India Country Director of Harvard's "
            "Mittal South Asia Institute.",
        "page_type": "ProfilePage",
        "og_type": "profile",
        "image": COMMENCEMENT,
        "image_size": (900, 1350),
        "image_alt": "Dr. Sanjay Kumar in cap and gown at Harvard commencement",
        "main_entity": PERSON,
        "extra": ["book"],
    },
    {
        "file": "fit.html",
        "path": "/fit",
        "crumb": "Right Fit",
        "title": "Right Fit, and Questions Families Ask | Blue Ocean Education",
        "description":
            "Who Blue Ocean works with, who it does not, and how joining "
            "works. Straight answers on cost, guarantees, grades, boards and "
            "the other companies called Blue Ocean.",
        "page_type": "WebPage",
        "og_type": "article",
        "extra": ["faq"],
    },
    {
        "file": "team.html",
        "path": "/team",
        "crumb": "Team",
        "title": "The Team and Board of Advisors | Blue Ocean Education",
        "description":
            "Four people on every file, led by founder Dr. Sanjay Kumar, over "
            "a board of advisors drawn from Harvard, MIT and LSE.",
        "page_type": "WebPage",
        "og_type": "article",
    },
    {
        "file": "start.html",
        "path": "/start",
        "crumb": "Request a Consultation",
        "title": "Request a Consultation | Blue Ocean Education",
        "description":
            "Book a diagnostic call with the Blue Ocean team. A short review "
            "of the student's profile and an honest answer on whether we are "
            "the right team for them.",
        "page_type": "ContactPage",
        "og_type": "website",
    },
    {
        "file": "privacy.html",
        "path": "/privacy",
        "crumb": "Privacy Policy",
        "title": "Privacy Policy | Blue Ocean Education",
        "description":
            "What Blue Ocean Education collects from families, why, who it "
            "goes to, and the rights the Digital Personal Data Protection "
            "Act, 2023 gives you over it.",
        "page_type": "WebPage",
        "og_type": "article",
    },
    # Reached only after a booking, and it carries a newsletter form and a
    # resource list rather than anything a search result should land on.
    # `follow` rather than `none` so the links out of it still pass.
    {
        "file": "next-steps.html",
        "path": "/next-steps",
        "crumb": "Next Steps",
        "title": "Next Steps | Blue Ocean Education",
        "description":
            "Your diagnostic call is booked. Here are the most useful next "
            "steps while a Blue Ocean advisor reviews the profile.",
        "page_type": "WebPage",
        "og_type": "website",
        "robots": "noindex, follow",
    },
    {
        "file": "404.html",
        "path": "/404",
        "crumb": "Page not found",
        "title": "Page not found | Blue Ocean Education",
        "description":
            "That page is not on blueoceanedu.com. The method, the results, "
            "the founder, the team, and how to join are all one click away.",
        "page_type": "WebPage",
        "og_type": "website",
        "robots": "noindex, follow",
        "minimal": True,
    },
]

DEFAULT_ROBOTS = ("index, follow, max-snippet:-1, max-image-preview:large, "
                  "max-video-preview:-1")


def esc(text):
    """Escape for an HTML attribute value."""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def graph_for(cfg):
    url = ORIGIN + cfg["path"]
    if cfg["path"] == "/":
        url = ORIGIN + "/"

    page = {
        "@type": cfg["page_type"],
        "@id": url + "#webpage",
        "url": url,
        "name": cfg["title"],
        "description": cfg["description"],
        "inLanguage": "en-IN",
        "isPartOf": {"@id": SITE},
        "about": {"@id": cfg.get("main_entity", ORG)},
        "primaryImageOfPage": cfg.get("image", OG_CARD),
        "publisher": {"@id": ORG},
    }
    if "main_entity" in cfg:
        page["mainEntity"] = {"@id": cfg["main_entity"]}

    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home",
               "item": ORIGIN + "/"}]
    if cfg["crumb"]:
        crumbs.append({"@type": "ListItem", "position": 2,
                       "name": cfg["crumb"], "item": url})
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}

    nodes = [page]
    if cfg["crumb"]:
        nodes.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
                      "itemListElement": crumbs})
    nodes.append(website())
    nodes.append(organisation(with_catalog=cfg.get("catalog", False)))
    nodes.append(person())

    for name in cfg.get("extra", []):
        if name == "book":
            nodes.append(book())
        elif name == "faq":
            nodes.append(faq_node(url))
            page["mainEntity"] = {"@id": url + "#faq"}
        else:
            sys.exit("build-seo: unknown extra node %r" % name)

    return {"@context": "https://schema.org", "@graph": nodes}


def block_for(cfg):
    url = ORIGIN + cfg["path"] if cfg["path"] != "/" else ORIGIN + "/"
    image = cfg.get("image", OG_CARD)
    iw, ih = cfg.get("image_size", (1200, 630))
    alt = cfg.get("image_alt", OG_CARD_ALT)
    robots = cfg.get("robots", DEFAULT_ROBOTS)

    lines = [
        OPEN,
        "  <!-- Generated by tools/build-seo.py. Do not hand-edit: the next run",
        "       overwrites everything between these two sentinels. Change the",
        "       PAGES list or a node builder in that file instead. -->",
        "  <title>%s</title>" % esc(cfg["title"]),
        '  <meta name="description" content="%s">' % esc(cfg["description"]),
        '  <meta name="robots" content="%s">' % esc(robots),
        '  <link rel="canonical" href="%s">' % url,
    ]

    if not cfg.get("minimal"):
        lines += [
            "",
            '  <meta property="og:type" content="%s">' % cfg["og_type"],
            '  <meta property="og:site_name" content="Blue Ocean Education">',
            '  <meta property="og:locale" content="en_IN">',
            '  <meta property="og:url" content="%s">' % url,
            '  <meta property="og:title" content="%s">' % esc(cfg["title"]),
            '  <meta property="og:description" content="%s">'
            % esc(cfg["description"]),
            '  <meta property="og:image" content="%s">' % image,
            '  <meta property="og:image:width" content="%d">' % iw,
            '  <meta property="og:image:height" content="%d">' % ih,
            '  <meta property="og:image:alt" content="%s">' % esc(alt),
        ]
        if cfg["og_type"] == "profile":
            lines += [
                '  <meta property="profile:first_name" content="Sanjay">',
                '  <meta property="profile:last_name" content="Kumar">',
            ]
        lines += [
            "",
            '  <meta name="twitter:card" content="summary_large_image">',
            '  <meta name="twitter:title" content="%s">' % esc(cfg["title"]),
            '  <meta name="twitter:description" content="%s">'
            % esc(cfg["description"]),
            '  <meta name="twitter:image" content="%s">' % image,
            '  <meta name="twitter:image:alt" content="%s">' % esc(alt),
        ]
        if cfg["file"] == "founder.html":
            lines.append('  <meta name="author" content="Dr. Sanjay Kumar">')

        graph = json.dumps(graph_for(cfg), indent=2, ensure_ascii=False)
        graph = "\n".join("  " + ln for ln in graph.splitlines())
        lines += ["", '  <script type="application/ld+json">', graph,
                  "  </script>"]

    lines.append("  " + CLOSE)
    return "\n".join("  " + ln if i == 0 else ln
                     for i, ln in enumerate(lines))


# The region a first run replaces: from <title> up to, but not including, the
# main stylesheet. Every page has exactly this shape, checked below.
FIRST_RUN = re.compile(
    r'  <title>.*?(?=  <link rel="stylesheet" href="main\.css">)', re.S)
SENTINELS = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.S)


def apply_to(html, cfg, where):
    block = block_for(cfg)
    if OPEN in html:
        if CLOSE not in html:
            sys.exit("build-seo: %s opens @seo and never closes it" % where)
        return SENTINELS.sub(lambda m: block.strip(), html, count=1)
    if not FIRST_RUN.search(html):
        sys.exit("build-seo: %s has no <title> ... main.css region to replace. "
                 "Add the @seo sentinels by hand and re-run." % where)
    return FIRST_RUN.sub(lambda m: block + "\n", html, count=1)


def main():
    check = "--check" in sys.argv
    stale, wrote = [], []
    for cfg in PAGES:
        path = ROOT / cfg["file"]
        if not path.is_file():
            sys.exit("build-seo: %s is in PAGES but not on disk" % cfg["file"])
        html = path.read_text()
        out = apply_to(html, cfg, cfg["file"])
        if out == html:
            continue
        if check:
            stale.append(cfg["file"])
        else:
            path.write_text(out)
            wrote.append(cfg["file"])

    if check:
        if stale:
            sys.exit("build-seo: out of date, run `python3 tools/build-seo.py`: "
                     + ", ".join(stale))
        print("build-seo: every page is current")
        return
    print("build-seo: wrote the @seo block into %d page%s"
          % (len(wrote), "" if len(wrote) == 1 else "s"))
    for name in wrote:
        print("  " + name)
    if not wrote:
        print("  (nothing changed)")


if __name__ == "__main__":
    main()

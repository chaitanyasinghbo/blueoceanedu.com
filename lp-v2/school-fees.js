/* Blue Ocean Education - school and fee reference data.
   Source: Indian_Schools_Fees_Complete_Reviewed_2026.csv, 2026 review.

   Fees are never rendered on the page. They are resolved at submit time and
   posted to the lead sheet only, so the team can read affordability off the
   row without asking a family about money on an intake form.

   Record shape: [schoolName, cityIndex, ibFeeINR, generalFeeINR]. A 0 means
   the source lists NA for that stream, not that the stream is free.

   "Paud, Pune district" is folded into Pune. It is one school, UWC Mahindra,
   and a city dropdown should not carry a district description as an option.

   The block between the generated markers below is written by
   tools/build-school-fees.py. Edit the CSV and re-run that, do not hand-edit
   the rows. Everything outside the markers is hand-written and is left
   alone by the generator. */
(function (root) {
  'use strict';

  /* --- generated:begin --- */

  var CITIES = [
    "Ahmedabad",
    "Ajmer",
    "Almora",
    "Bengaluru",
    "Chandigarh",
    "Chennai",
    "Dehradun",
    "Durgapur",
    "Gurugram",
    "Gwalior",
    "Hyderabad",
    "Jaipur",
    "Jhajjar",
    "Kodaikanal",
    "Kolhapur",
    "Lucknow",
    "Madanapalle",
    "Mumbai",
    "Mussoorie",
    "Nainital",
    "New Delhi",
    "Noida",
    "Ooty",
    "Panchgani",
    "Pilani",
    "Pune",
    "Rohtak",
    "Shimla",
    "Solan",
    "Sonipat"
  ];

  /* [name, cityIndex, ibFee, generalFee] */
  var SCHOOLS = [
    ["Adani International School – Shantigram", 0, 572749, 0],
    ["Ahmedabad International School", 0, 361800, 160950],
    ["Mayo College", 1, 0, 1152000],
    ["Mayo College Girls' School", 1, 0, 1152000],
    ["Ashok Hall Girls' Residential School", 2, 0, 473000],
    ["Aadya Academy – The Residential School", 3, 0, 270000],
    ["Bethany High School – Koramangala", 3, 0, 72000],
    ["Canadian International School – Yelahanka", 3, 1030000, 0],
    ["Ebenezer International School Bangalore – Electronic City", 3, 320000, 420000],
    ["Head Start Educational Academy – Dommasandra", 3, 0, 420000],
    ["Indus International School – Sarjapur", 3, 767500, 767500],
    ["Legacy School – Byrathi Village", 3, 550000, 0],
    ["One World International School – Sarjapur", 3, 600000, 0],
    ["Stonehill International School – North Bengaluru", 3, 2024271, 0],
    ["The Academic City School – Bengaluru", 3, 0, 549000],
    ["The International School Bangalore", 3, 1060000, 0],
    ["Trio World Academy – Sahakar Nagar", 3, 300000, 0],
    ["Firststeps School – Sector 26", 4, 0, 205000],
    ["American International School Chennai", 5, 2813831, 2813831],
    ["Chettinad Sarvalokaa Education – Kelambakkam", 5, 0, 450000],
    ["HLC International School – Karanai", 5, 0, 420000],
    ["Hiranandani Upscale School – Uthandi", 5, 490000, 0],
    ["Vaels International School – Injambakkam", 5, 0, 0],
    ["Cambrian Hall School", 6, 0, 595000],
    ["Ecole Globale International Girls' School", 6, 0, 1048130],
    ["The Doon School", 6, 1654000, 1454000],
    ["The TonsBridge School", 6, 0, 87000],
    ["Unison World School", 6, 0, 1120000],
    ["Welham Boys' School", 6, 0, 570000],
    ["Welham Girls' School", 6, 0, 1110000],
    ["Delhi Public School Durgapur", 7, 0, 84550],
    ["Amity Global School – Gurgaon", 8, 421000, 0],
    ["Amity International School – Gurgaon Sector 46", 8, 0, 162330],
    ["DPS International – Sector 50", 8, 869848, 0],
    ["Excelsior American School – Sector 43", 8, 1358220, 0],
    ["GD Goenka World School – Sohna", 8, 322908, 322908],
    ["GEMS International School – Palam Vihar", 8, 333440, 333440],
    ["Heritage Xperiential Learning School – Sector 62", 8, 0, 532000],
    ["Kunskapsskolan International School", 8, 0, 424840],
    ["Lancers International School – Sector 53 / DLF Phase 5", 8, 1536000, 0],
    ["Manav Rachna International School – Sector 46", 8, 0, 296600],
    ["MatriKiran High School – Sector 83", 8, 0, 234750],
    ["Pathways School – Gurgaon", 8, 1528000, 0],
    ["Pathways World School – Sohna / Aravali", 8, 1485000, 0],
    ["Scottish High International School – Sector 57", 8, 929244, 519312],
    ["Shikshantar School – Sector 41", 8, 0, 232190],
    ["Shiv Nadar School – Sector 26A", 8, 1035500, 420652],
    ["The Shri Ram School – Aravali", 8, 0, 346000],
    ["The Shri Ram School – Moulsari", 8, 0, 320000],
    ["Scindia Kanya Vidyalaya", 9, 0, 841000],
    ["The Scindia School – Fort Campus", 9, 0, 1071500],
    ["Ambitus World School – Bachupally", 10, 0, 212982],
    ["CHIREC International School – Serilingampally", 10, 644000, 0],
    ["Delhi Public School – Nacharam", 10, 0, 260183],
    ["International School of Hyderabad", 10, 1359450, 0],
    ["Keystone School – Puppalaguda", 10, 0, 467000],
    ["Oakridge International School – Gachibowli", 10, 753500, 560000],
    ["The Aga Khan Academy Hyderabad – Hardware Park", 10, 1466500, 0],
    ["Jayshree Periwal International School", 11, 504900, 0],
    ["Neerja Modi School", 11, 200000, 181600],
    ["Sehwag International School", 12, 0, 140000],
    ["Kodaikanal International School", 13, 2025000, 2025000],
    ["Sanjay Ghodawat International School – Atigre", 14, 0, 170000],
    ["La Martiniere College", 15, 0, 102880],
    ["Rishi Valley School", 16, 0, 875000],
    ["Aditya Birla World Academy", 17, 1100000, 1100000],
    ["American School of Bombay", 17, 3590194, 3590194],
    ["Ascend International School – Bandra East", 17, 1300000, 0],
    ["B.D. Somani International School – Cuffe Parade", 17, 1100000, 0],
    ["Bombay International School – Malabar Hill", 17, 1000000, 0],
    ["Bombay Scottish School", 17, 0, 105000],
    ["Dhirubhai Ambani International School", 17, 965000, 448000],
    ["Ecole Mondiale World School", 17, 1090000, 0],
    ["Edubridge International School – Girgaon", 17, 365004, 0],
    ["Fazlani L'Academie Globale – Mazgaon", 17, 0, 650000],
    ["Hill Spring International School – Tardeo", 17, 600000, 600000],
    ["JBCN International – Oshiwara", 17, 774850, 0],
    ["JBCN International – Parel", 17, 860850, 0],
    ["Jamnabai Narsee International School", 17, 1000000, 0],
    ["Mainadevi Bajaj International School – Malad", 17, 0, 279500],
    ["Mount Litera School International – Bandra East", 17, 900000, 0],
    ["Nahar International School – Andheri East", 17, 500000, 0],
    ["Oberoi International School – JVLR", 17, 1200000, 0],
    ["Oberoi International School – OGC", 17, 1200000, 0],
    ["Prabhavati Padamshi Soni International Junior College – Juhu", 17, 0, 447000],
    ["Guru Nanak Fifth Centenary School – Shangri-La Girls", 18, 0, 245000],
    ["Mussoorie International School", 18, 1200000, 1100000],
    ["Woodstock School", 18, 1765000, 0],
    ["Sherwood College", 19, 0, 650000],
    ["American Embassy School – Chanakyapuri", 20, 3813253, 3813253],
    ["Amity International School – Pushp Vihar", 20, 0, 113928],
    ["Apeejay School International – Panchsheel Park", 20, 791499, 0],
    ["DPS International School – Pushp Vihar", 20, 0, 360960],
    ["G.D. Goenka Public School – Rohini", 20, 0, 197984],
    ["GD Goenka Public School – Vasant Kunj", 20, 0, 237800],
    ["K.R. Mangalam Global School – Greater Kailash I", 20, 792000, 0],
    ["Modern School – Barakhamba Road", 20, 0, 209600],
    ["Modern School – Vasant Vihar", 20, 0, 258060],
    ["Amity Global School – Noida", 21, 614640, 614640],
    ["Amity International School – Noida", 21, 0, 195732],
    ["Apeejay School – Sector 16A", 21, 0, 220951],
    ["Genesis Global School – Sector 132", 21, 907200, 550800],
    ["Gyanshree School – Sector 127", 21, 0, 241200],
    ["Prometheus School – Sector 131", 21, 1110000, 926000],
    ["Good Shepherd International School", 22, 1950000, 1700000],
    ["The Lawrence School, Lovedale", 22, 0, 710000],
    ["Billimoria High School", 23, 0, 635960],
    ["Birla School Pilani", 24, 0, 477730],
    ["B.K. Birla Centre for Education", 25, 0, 450000],
    ["MIT Vishwashanti Gurukul World School – Loni Kalbhor", 25, 480000, 0],
    ["Mahindra International School – Hinjawadi", 25, 1763000, 0],
    ["UWC Mahindra College – Paud", 25, 2875000, 0],
    ["Universal Wisdom School – Balewadi", 25, 0, 0],
    ["Wellington College International Pune – Wagholi", 25, 800000, 0],
    ["GD Goenka International School – Rohtak", 26, 0, 162000],
    ["Bishop Cotton School", 27, 0, 920000],
    ["The Lawrence School, Sanawar", 28, 0, 1070800],
    ["Swarnprastha Public School", 29, 0, 171600],
  ];

  /* --- generated:end --- */

  /* Boards that put a student on the international fee line at these schools.
     The source has two fee columns, an IB one and a general one, so every
     board has to resolve to one of them. IGCSE, A Levels and AP are priced
     with the international stream wherever a school runs both. */
  var INTERNATIONAL_BOARDS = ['ib', 'igcse', 'alevels', 'ap'];

  /* Words that carry no identifying signal in an Indian school name. Stripped
     before a typed name is compared with the list, so "The Doon School" and
     "Doon" match on the one token that distinguishes them. */
  var STOPWORDS = {
    school: 1, schools: 1, international: 1, intl: 1, the: 1, of: 1, and: 1,
    academy: 1, college: 1, public: 1, high: 1, senior: 1, secondary: 1,
    global: 1, world: 1, education: 1, educational: 1, campus: 1, sector: 1,
    institute: 1, vidyalaya: 1, vidya: 1, mandir: 1, residential: 1,
    junior: 1, for: 1, centre: 1, center: 1, learning: 1, city: 1,
    national: 1, model: 1, new: 1, road: 1, phase: 1, block: 1, no: 1
  };

  function normalise(value) {
    return String(value || '')
      .toLowerCase()
      .replace(/[‐-―]/g, ' ')
      .replace(/[^a-z0-9]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function significantTokens(value, extraStop) {
    var stop = extraStop || {};
    return normalise(value).split(' ').filter(function (token) {
      return token.length > 1 && !STOPWORDS[token] && !stop[token];
    });
  }

  function record(index) {
    var row = SCHOOLS[index];
    return {
      name: row[0],
      city: CITIES[row[1]],
      ibFee: row[2],
      generalFee: row[3]
    };
  }

  function cityList() {
    return CITIES.slice();
  }

  function schoolsInCity(city) {
    var wanted = normalise(city);
    var out = [];
    for (var i = 0; i < SCHOOLS.length; i++) {
      if (normalise(CITIES[SCHOOLS[i][1]]) === wanted) out.push(record(i));
    }
    return out;
  }

  function findExact(name) {
    var wanted = normalise(name);
    if (!wanted) return null;
    for (var i = 0; i < SCHOOLS.length; i++) {
      if (normalise(SCHOOLS[i][0]) === wanted) return record(i);
    }
    return null;
  }

  /* A typed school name is matched on the tokens that survive the stopword
     list, scored against both directions so a short entry ("Doon") and a long
     one ("The Doon School Dehradun main campus") both land. The city is a
     tiebreaker, never a filter: families mistype the city more often than the
     school. */
  function findFuzzy(name, city) {
    var extraStop = {};
    significantTokens(city).forEach(function (token) { extraStop[token] = 1; });

    var queryTokens = significantTokens(name, extraStop);
    if (!queryTokens.length) return null;

    var queryFull = normalise(name);
    var cityNorm = normalise(city);
    var best = null;

    for (var i = 0; i < SCHOOLS.length; i++) {
      var candidateTokens = significantTokens(SCHOOLS[i][0], extraStop);
      if (!candidateTokens.length) continue;

      var shared = 0;
      for (var q = 0; q < queryTokens.length; q++) {
        if (candidateTokens.indexOf(queryTokens[q]) !== -1) shared++;
      }
      if (!shared) continue;

      var score = shared / Math.min(queryTokens.length, candidateTokens.length);
      var candidateFull = normalise(SCHOOLS[i][0]);
      if (candidateFull.indexOf(queryFull) !== -1 || queryFull.indexOf(candidateFull) !== -1) {
        score = Math.max(score, 0.9);
      }
      if (cityNorm && normalise(CITIES[SCHOOLS[i][1]]) === cityNorm) score += 0.08;

      /* Ties break on the raw count of shared tokens, so "Mayo College Girls"
         lands on the Girls' school rather than on whichever Mayo row the list
         happens to hold first. */
      if (!best || score > best.score + 1e-9 ||
          (Math.abs(score - best.score) < 1e-9 && shared > best.shared)) {
        best = { index: i, score: score, shared: shared };
      }
    }

    if (!best || best.score < 0.62) return null;
    var hit = record(best.index);
    hit.score = Math.round(Math.min(best.score, 1) * 100) / 100;
    return hit;
  }

  /* The one call the form makes. Returns everything the sheet needs to explain
     the number it was given, including how the match was made, so a wrong
     match is auditable rather than invisible. */
  function resolveFee(schoolName, city, board) {
    var result = {
      matchedName: '',
      matchedCity: '',
      matchMethod: 'none',
      matchScore: '',
      feeBasis: '',
      /* Both source columns exactly as the CSV publishes them, blank where it
         says NA. They ship alongside the resolved figure so the sheet always
         carries the raw numbers and never only a derived one. */
      ibFee: '',
      generalFee: '',
      annualFee: '',
      feeBand: 'Unknown'
    };
    if (!schoolName) return result;

    var hit = findExact(schoolName);
    if (hit) {
      result.matchMethod = 'exact';
      result.matchScore = 1;
    } else {
      hit = findFuzzy(schoolName, city);
      if (hit) {
        result.matchMethod = 'fuzzy';
        result.matchScore = hit.score;
      }
    }
    if (!hit) return result;

    result.matchedName = hit.name;
    result.matchedCity = hit.city;
    result.ibFee = hit.ibFee || '';
    result.generalFee = hit.generalFee || '';

    var wantsInternational = INTERNATIONAL_BOARDS.indexOf(board) !== -1;
    var primary = wantsInternational ? hit.ibFee : hit.generalFee;
    var fallback = wantsInternational ? hit.generalFee : hit.ibFee;

    if (primary) {
      result.annualFee = primary;
      result.feeBasis = wantsInternational ? 'IB / international stream' : 'General stream';
    } else if (fallback) {
      result.annualFee = fallback;
      result.feeBasis = (wantsInternational ? 'General stream' : 'IB / international stream') +
        ' (only stream published for this school)';
    } else {
      result.feeBasis = 'No fee published';
      return result;
    }

    result.feeBand = band(result.annualFee);
    return result;
  }

  /* Bands, not the raw number, are what a first read of the sheet needs. */
  function band(amount) {
    if (!amount) return 'Unknown';
    if (amount >= 1500000) return 'A. 15L+';
    if (amount >= 1000000) return 'B. 10L to 15L';
    if (amount >= 600000) return 'C. 6L to 10L';
    if (amount >= 300000) return 'D. 3L to 6L';
    if (amount >= 150000) return 'E. 1.5L to 3L';
    return 'F. Under 1.5L';
  }

  root.BOSchools = {
    cities: cityList,
    inCity: schoolsInCity,
    findExact: findExact,
    findFuzzy: findFuzzy,
    resolveFee: resolveFee,
    feeBand: band,
    count: SCHOOLS.length
  };
}(window));

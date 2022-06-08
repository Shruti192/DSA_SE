//Requiring the modules -> It should always be done on the top
const express = require("express");
const ejs = require("ejs"); //View Engine
const path = require("path");
const { spawn } = require("child_process");
var bodyParser = require("body-parser");
const fs = require("fs");
const { removeStopwords, eng, fra } = require("stopword");
const { readFileSync, promises: fsPromises } = require("fs");
const { zho } = require("stopword");
const stem = require("stem-porter");
var SpellCorrector = require("spelling-corrector");
var spellCorrector = new SpellCorrector();
spellCorrector.loadDictionary();

//Creating our server
const app = express();

//Setting Up EJS
app.set("view engine", "ejs");

const PORT = process.env.PORT || 3000;
var urlencodedParser = bodyParser.urlencoded({ extended: false });

// middleware & static files
app.use(express.static(path.join(__dirname, "/public")));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
var jsonParser = bodyParser.json();

function nl2br(str, is_xhtml) {
  var breakTag =
    is_xhtml || typeof is_xhtml === "undefined" ? "<br />" : "<br>";
  return (str + "").replace(
    /([^>\r\n]?)(\r\n|\n\r|\r|\n)/g,
    "$1" + breakTag + "$2"
  );
}
//@GET /
//description: GET request to home page
app.get("/", (req, res) => {
  res.render("index", { heading: "Home Page" });
});

app.get("/search", (req, res) => {
  var query = req.query.question;
  /*  Preparing Query Keywords!!  */
  var str = query.toLowerCase();
  str = str.replace(/(\r\n|\n|\r|[^a-zA-Z0-9 ])/gm, "");
  str = str.split(" ");
  var str1 = removeStopwords(str);
  var keyQ = [];
  for (var i = 0; i < str1.length; i++) {
    var correct_spell = spellCorrector.correct(str1[i]);
    var stem_element = stem(correct_spell);
    keyQ.push(stem_element);
  }
  keyQ.sort();
  // console.log(`These are query keywords:- ${keyQ}`);
  var N = 1300; //Size of corpus.
  var mp_query = new Map();
  keyQ.forEach((element) => {
    if (mp_query.has(element)) {
      mp_query.set(element, mp_query.get(element) + 1);
    } else {
      mp_query.set(element, 1);
    }
  });
  // console.log(`This is query Map :-`);
  // console.log(mp_query);
  var M = keyQ.length; //sz_query_keywords

  /* ********* Score(D,Q) = Score of Doucument D for given query_keyword_array Q  ************ 
   We will calculate score(D,Q) for each document in our corpus as per BM25 similarity
   reference to maths of BM25: https://kmwllc.com/index.php/2020/03/20/understanding-tf-idf-and-bm-25/
    According to formulae things i need to collect or calculate for BM25 Score calculation are:-
      #   parameter b= 0.75 and k1 = 1.5
      #   f(q, D) = term frequency = frequency of keyword q in doc D (MP it will be a 2-D array kinda thing with each row representing D's and each coloumn representing q's) 
      # df(q) or n(q) i.e Document frequency
      #  IDF(q) = it will be a row 
      # i already have |D| value for each doc stored in All_doc_len.txt and using which i have to calculate avg_dl    */
  // df(q) array calculation
  var df = [];
  keyQ.forEach((q) => {
    var cnt = 0;
    for (var i = 1; i < N + 1; i++) {
      var key = fs
        .readFileSync(
          "Problem_Set/Problem_keywords/kewords_" + i.toString() + ".txt"
        )
        .toString()
        .split("\n");
      if (key.includes(q)) {
        cnt += 1;
      }
    }
    df.push(cnt);
  });
  // console.log(`df_row: ${df}`);
  // IDF(q) array calculation
  idf = [];
  for (var i = 0; i < df.length; i++) {
    var x = 1 + (N - df[i] + 0.5) / (df[i] + 0.5);
    if (x != NaN) {
      idf.push(Math.log10(x));
    } else {
      idf.push(0);
    }
  }
  // console.log(`idf_row: ${idf}`);
  // score(D) calculation along with f(q,D) calculation
  var doc_len = fs
    .readFileSync("Problem_Set/All_doc_len.txt")
    .toString()
    .split("\n");
  var avg_dl = 0.0;
  for (var i = 0; i < N; i++) {
    avg_dl += parseFloat(doc_len[i]);
  }
  avg_dl /= N;
  // console.log(`avg_dl: ${avg_dl}`);
  var k1 = 1.5;
  var b = 0.75;
  var score = new Map();

  /*  ***************   score calculation ***************    */
  for (var i = 1; i < N + 1; i++) {
    var data = readFileSync(
      "Problem_Set/Problem_dict/dict_" + i.toString() + ".txt"
    ).toString();
    data = data.replace(/,|:|"|{|}/g, "");
    data1 = data.split(" ");
    // console.log(data1);
    var key_map_doc = new Map();
    for (var j = 0; j < data1.length - 1; j += 2) {
      key_map_doc[data1[j]] = Number(data1[j + 1]);
    }
    // console.log(key_map_doc);
    var s = 0;
    keyQ.forEach((q) => {
      if (q in key_map_doc) {
        var f = key_map_doc[q]; //f(q,D)
        var t = k1 + 1;
        var p = 1 - b;
        var q = parseFloat(b / avg_dl);
        q *= parseFloat(doc_len[i]);
        p += q;
        p *= k1;
        p += f;
        f *= t;
        var z = parseFloat(f / p);
        if (!isNaN(z)) {
          s += z;
        } else {
          s += 0;
        }
      }
    });
    score.set(s, i);
  }
  const Sscore = new Map([...score.entries()].sort().reverse());
  // console.log(Sscore);
  var id_ = [];
  var sc_ = [];
  Sscore.forEach((v, k) => {
    sc_.push(k);
    id_.push(v);
  });
  // for (var i = 0; i < 10; i++) {
  //   console.log(`${id_[i]} : ${sc_[i]}`);
  // }
  arr = [];
  for (var i = 0; i < 10; i++) {
    var _id = id_[i];
    var T = fs
      .readFileSync(
        "Problem_Set/Problem_titles/problem_title_" + _id.toString() + ".txt"
      )
      .toString();
    var U = fs
      .readFileSync(
        "Problem_Set/Problem_urls/problem_url_" + _id.toString() + ".txt"
      )
      .toString();
    var des = fs
      .readFileSync(
        "Problem_Set/Problem_Content/problem_" + _id.toString() + ".txt"
      )
      .toString();
    des = des.replace(/(\r\n|\n|\r)/gm, "");
    des = des.replace(/[^a-zA-Z0-9 ]/g, "");
    if (des[0] == "b") {
      des = des.replace(des[0], "");
    }
    des = des.slice(0, 300);
    arr.push({
      id: _id,
      title: T,
      url: U,
      statement: des,
    });
  }
  // console.log(arr);
  res.json(arr);
});

app.get("/detail/:id", (req, res) => {
  try {
    var id_ = req.params.id;
    var T = fs
      .readFileSync("Problem_Set/Problem_titles/problem_title_" + id_ + ".txt")
      .toString();
    var site = fs
      .readFileSync("Problem_Set/Problem_urls/problem_url_" + id_ + ".txt")
      .toString();
    var des = fs
      .readFileSync("Problem_Set/Problem_Content/problem_" + id_ + ".txt")
      .toString();
    var ppp = des.split("\\n");
    for (var i = 0; i < 40; i++) {
      ppp.pop();
    }
    ppp.shift();
    var new_desc = "";
    for (var i = 0; i < ppp.length; i++) {
      if (ppp[i] === "") {
        new_desc += "\n";
      } else {
        new_desc += ppp[i];
      }
    }
    new_des = nl2br(new_desc);
    new_des = new_des.replace(/[&\/\\#, +()$~%.'":*?{}]/g, " ");
    res.render("detail", {
      title: T,
      url_: site,
      content: new_des,
      heading: "Problem_details",
    });
  } catch (err) {
    res.render("error");
  }
});
app.get("/error", (req, res) => {
  try {
    res.render("error", { heading: "Error Page" });
  } catch (err) {
    res.send(`sorry we ran into problem!!! ${err}`);
  }
});

// 404 page
app.use((req, res) => {
  res.status(404).render("error", { heading: "Error Page" });
});

//Assigning Port to our application
app.listen(PORT, () => {
  console.log("Server is running on port " + PORT);
});

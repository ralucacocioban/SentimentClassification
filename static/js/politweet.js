function debateClean(d) {
  d.date = moment(
    "27 September 2008 " + d.date,
    "DD MMMM YYYY hh:mm:ss"
  ).add(1, 'hour')
  return d
}

function tweetsClean(d) {
  d["date"] = moment(
    d["pub.date.GMT"],
    "M/DD/YY h:mm"
  )
  delete d["pub.date.GMT"];
  return d
}
var i = 0;
function divideTweetsByDebate(tweets, debate) {
  var splits = []
  var tweets_count = 0;

  debate.forEach(function(sentence, i) {
    var during = []
    while(
      tweets[tweets_count]
      && +tweets[tweets_count].date < +sentence.date
    ) {
      during.push(tweets[tweets_count])
      tweets_count++;
    }
    splits.push({
      debate:debate[i-1] ? debate[i-1] : {who:"Before the show"},
      tweets:during
    })
  });

  splits.push({
    debate: debate[debate.length-1],
    tweets: []
  })
  splits.push({
    debate: {who:"After the show"},
    tweets: tweets.slice(tweets_count-1)
  })
  return splits
}

var politweet = angular.module("politweet", ['n3-pie-chart'])
  .controller("Debate", function() {

  })
  .controller("Main", function($scope) {
    $scope.debate = []
    $scope.tweets = []
    $scope.countSentiment = function(s) {
      var pos_oba = 0;
      var neg_oba = 0;
      var pos_mcc = 0;
      var neg_mcc = 0;
      var oth_oba = 0;
      var oth_mcc = 0;
      var padding_oba = 0;
      var padding_mcc = 0;
      var other = 0;
      for (var i=0; i < s.length; i++) {
        var t = s[i];
        if (t["sent_tfidf"] == 'neg') {
          if (t["candidate"] == 'oba') {
            neg_oba++
          }
          else if (t["candidate"] == 'mcc') {
            neg_mcc++
          }
          else {
            other++
          }
        }
        else if (t["sent_tfidf"] == 'pos') {
          if (t["candidate"] == 'oba') {
            pos_oba++
          }
          else if (t["candidate"] == 'mcc') {
            pos_mcc++
          }
          else {
            other++
          }
        } else if (t["sent_tfidf"] == 'other') {
          if (t["candidate"] == 'oba') {
            oth_oba++
          }
          else if (t["candidate"] == 'mcc') {
            oth_mcc++
          }
          else {
            other++
          }
        }
      }

      if (pos_oba + neg_oba + oth_oba == 0 ) {
        padding_oba = 1
      }
      if (pos_mcc + neg_mcc + oth_mcc == 0) {
        padding_mcc = 1
      }

      return {
        pos_oba:pos_oba,
        neg_oba:neg_oba,
        pos_mcc:pos_mcc,
        neg_mcc:neg_mcc,
        oth_oba:oth_oba,
        oth_mcc:oth_mcc,
        padding_oba: padding_oba,
        padding_mcc: padding_mcc
      }
    }
    d3.csv('debatetranscript.csv', debateClean, function(err, debate) {

      d3.csv('worked.csv', tweetsClean, function(err, tweets) {
        $scope.$apply(function() {
          $scope.debate = debate
          $scope.tweets = tweets
          $scope.splits = divideTweetsByDebate(tweets, debate)
        })
      })
    })
  })
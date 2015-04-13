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
      debate:debate[i-1] ? debate[i-1] : {who:"begins"},
      tweets:during
    })
  });

  splits.push({
    debate: debate[debate.length-1],
    tweets: tweets.slice(tweets_count-1)
  })
  return splits
}

var politweet = angular.module("politweet", [])
  .controller("Debate", function() {

  })
  .controller("Main", function($scope) {
    $scope.debate = []
    $scope.tweets = []
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
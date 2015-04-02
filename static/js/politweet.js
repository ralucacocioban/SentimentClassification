var politweet = angular.module("politweet", [])
  .controller("Debate", function() {

  })
  .controller("Main", function($scope) {
    $scope.debate = [{
        sentence: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet mattis diam. Integer sit amet laoreet ex. Curabitur venenatis, mi a vulputate consectetur, nunc turpis pulvinar turpis, id aliquet dui neque non tellus. Vivamus sollicitudin, metus nec varius tincidunt, lectus tellus dictum nibh, id bibendum nisl mauris convallis massa. Proin vel ante at neque scelerisque dapibus sed at nibh. ",
        analysis: {}
      }, {
        sentence: "Aenean accumsan vulputate mi, aliquam pulvinar dolor mollis id. Aenean egestas augue eu blandit lacinia. Integer varius felis orci, sit amet vestibulum elit vestibulum eu. Morbi cursus lacinia elit sed mollis. Maecenas nec ultricies ipsum. Cras vestibulum elementum diam sit amet elementum.",
        analysis: {}
      }]
  })
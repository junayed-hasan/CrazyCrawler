angular.module('userProfile', ['ngMaterial', 'ngMessages'])
  .controller('Ctrl', function($scope) {
    $scope.viewMode = true;
  
    // Switch between view mode and edit mode
    $scope.switchMode = function() {
      return $scope.viewMode = !$scope.viewMode;
    };
  
    // Save the changes
    $scope.saveChanges = function() {
      /*Validate the input
      Save the changes*/
    };
  
    // User data
    $scope.user = {
      name: 'Anika Jawhar',
      gender: 'Female',
      birthday: 'July 7, 2000',
      phone: '01799977711',
      email: 'jawhar700@gmail.com',
      otherEmail: 'anikaj0207@yahoo.com'
    }
  });
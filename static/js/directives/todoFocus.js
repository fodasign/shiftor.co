ineedtodo.directive("todoFocus", function ($timeout) {
    return function ($scope, element, attributes) {
        $scope.$watch(attributes.todoFocus, function (newVal) {
            if (newVal) {
                $timeout(function () {
                    element[0].focus()
                }, 0, false)
            }
        })
    }
})
ineedtodo.directive("todoBlur", function () {
    return function ($scope, element, attributes) {
        element.bind("blur", function () {
            $scope.$apply(attributes.todoBlur)
        })
    }
})
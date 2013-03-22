ineedtodo.controller("TodoController", function TodoController($scope, $resource) {

    $scope.todolist = $resource(
        "/api/:action/:subaction/:subsubaction/:quatrosubaction",
        {action: "items"}
    )

    $scope.todos = $scope.todolist.get()

    $scope.editedTodo = null

    $scope.getTotalTodos = function () {
        if ($scope.todos.items) {
            return $scope.todos.items.length
        }
        return 0
    }

    $scope.getTotalCompleted = function () {
        var completed = _.where($scope.todos.items, {completed: true})
        return completed.length
    }

    $scope.addTodo = function () {
        if ($scope.formTodoText != undefined && $scope.formTodoText != "") {
            $scope.todos.$save(
                {action: "item", subaction: "add", title: $scope.formTodoText},
                function (result) {
                    console.log(result)
                    if (result["ok"] == 0) {
                        console.log("Error")
                    }
                }
            )
        }

        $scope.formTodoText = ""
    }

    $scope.toggleCompleted = function (todo) {
        if (todo.completed) {
            $scope.todos.$save(
                {action: "item", subaction: "complete", subsubaction: todo.pk},
                function (result) {
                    console.log(result)
                    if (result["ok"] == 0) {
                        console.log("Error")
                    }
                }
            )
        } else {
            $scope.todos.$save(
                {action: "item", subaction: "complete", subsubaction: todo.pk, quatrosubaction: "undo"},
                function (result) {
                    console.log(result)
                    if (result["ok"] == 0) {
                        console.log("Error")
                    }
                }
            )
        }
    }

    $scope.clearCompleted = function () {
        var completed = _.filter($scope.todos.items, function (todo) {
            return todo.completed
        })

        _.each(completed, function (todo) {
            $scope.todos.$save(
                {action: "item", subaction: "archive", subsubaction: todo.pk},
                function (result) {
                    console.log(result)
                    if (result["ok"] == 0) {
                        console.log("Error")
                    }
                }
            )
        })
    }

    $scope.deleteTodo = function (todo) {
        $scope.todos.$delete(
            {action: "item", subaction: "delete", subsubaction: todo.pk},
            function (result) {
                console.log(result)
                if (result["ok"] == 0) {
                    console.log("Error")
                }
            }
        )
    }

    $scope.editTodo = function (todo) {
        $scope.editedTodo = todo
    }

    $scope.doneEditing = function (todo) {
        if (!todo.title) {
            var confirmDelete = confirm("Leaving this blank will delete this item. Are you sure you want to delet this item?")
            if (confirmDelete) {
                $scope.deleteTodo(todo)
            } else {
                $scope.todos.$save(
                    {action: "item", subaction: "edit", subsubaction: todo.pk, title: "Empty"},
                    function (result) {
                        console.log(result)
                        if (result["ok"] == 0) {
                            console.log("Error")
                        }
                    }
                )
            }
        } else  {
            $scope.todos.$save(
                {action: "item", subaction: "edit", subsubaction: todo.pk, title: todo.title},
                function (result) {
                    console.log(result)
                    if (result["ok"] == 0) {
                        console.log("Error")
                    }
                }
            )
        }

        $scope.editedTodo = null
    }

})


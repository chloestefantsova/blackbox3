var global_tasks = [];
var $task_panel = null;
var task_submit_url = null;

var getTaskByPk = function (pk) {
    global_tasks.forEach(function (task) {
        console.log('pk='+pk);
        console.log('task.pk='+task.pk);
        if (task.pk == pk) {
            return task;
        }
    });
    return null;
};

var refreshTaskList = function ($root) {
    var $list = $('<ul>').addClass('list-unstyled');

    global_tasks.forEach(function (task) {
        var text = '('+task.category+' '+task.cost+') '+task.title;
        var $item = $('<li>');
        var $link = $('<a>')
            .addClass('task-link')
            .attr('href', '#tasks/'+task.pk)
            .text(text);
        $link.click(function (e) {
            if ($task_panel === null) {
                return;
            }

            var $task = $('<div>');
            var $title = $('<h3>').text(task.title);
            var $body = $(task.desc);
            $task.append($title).append($body);

            var $submitBtn = null;
            $submitForm = $('<form>')

                .attr('id', 'flag-submit-form')

                .append($('<input>')
                            .attr('type', 'hidden')
                            .attr('name', 'task')
                            .attr('value', task.pk))

                .append($('<input>')
                            .addClass('form-control')
                            .attr('type', 'text')
                            .attr('name', 'flag')
                            .attr('placeholder', 'Flag'))

                .append($submitBtn = $('<input>')
                            .attr('id', 'flag-submit-btn')
                            .attr('type', 'submit')
                            .attr('value', 'Submit Flag')
                            .addClass('btn')
                            .addClass('btn-primary'))

                .append($('<div>')
                            .attr('id', 'results'));

            $task_panel.children().remove();
            $task_panel.append($task);
            $task.append($submitForm);

            var submitForm = new Form($submitForm);

            $submitBtn.click(function (e) {
                e.preventDefault();
                $.ajax({
                    method: 'POST',
                    url: task_submit_url,
                    data: submitForm.getJson(),
                    success: function (data, stat, xhr) {
                        var resp = JSON.parse(xhr.responseText);
                        if ('error' in resp) {
                            $('#results').append($('<h1>').text('Error: '+resp['error']));
                        } else {
                            $('#results').append($('<h1>').text('Result: '+resp['result']));
                        }
                    },
                    error: function (xhr) {
                        var resp = JSON.parse(xhr.responseText);
                        $('#results').append($('<h1>').text('Error: '+resp['error']));
                    }
                });
            });
        });
        $item.append($link);
        $list.append($item);
    });

    $root.children().remove();
    $root.append($list);
};

var updateTaskList = function (url, $root) {
    $.ajax({
        method: 'GET',
        url: url,
        dataType: 'json',
        success: function (data, stat, xhr) {
            global_tasks = JSON.parse(xhr.responseText);
            refreshTaskList($root);
        }
    });
};

var setTaskPanel = function ($obj) {
    $task_panel = $obj;
}

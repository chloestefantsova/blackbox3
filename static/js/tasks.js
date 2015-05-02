var global_tasks = [];
var $task_panel = null;

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
            .attr('href', '#')
            .data('task-pk', task.pk)
            .text(text);
        $link.click(function (e) {
            e.preventDefault();
            if ($task_panel === null) {
                return;
            }

            var $task = $('<div>');
            var $title = $('<h3>').text(task.title);
            var $body = $(task.desc);
            $task.append($title).append($body);

            $task_panel.children().remove();
            $task_panel.append($task);
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

var populateTable = function ($el, teams) {
    teams.forEach(function (team) {
        var $row = $('<tr>');
        $row.append($('<td>').text(team.name));
        $row.append($('<td>').append(
            $('<img>').attr('src', team.flag)
        ));
        $el.append($row);
    })
}

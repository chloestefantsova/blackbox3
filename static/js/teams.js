var populateTable = function ($el, teams) {
    teams.forEach(function (team) {
        var $row = $('<tr>');
        $row.append($('<td>').text(team.name));
        if (team.flag) {
            $row.append($('<td>').append(
                $('<img>').attr('src', team.flag)
            ));
        } else {
            $row.append($('<td>').text('N/A'));
        }
        $el.append($row);
    })
}

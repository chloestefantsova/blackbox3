var fadeInAll = function ($el) {
    var promise = $el.find('.faded1').fadeIn('slow').promise();
    var continuations = new Array();
    [1, 2, 3, 4, 5, 6, 7, 8, 9].forEach(function (i) {
        continuations.push(function () {
            console.log('working with .faded'+i);
            return $el.find('.faded'+i).fadeIn('slow').promise();
        });
    });
    promisePipe(promise, continuations).then(function () {
        console.log('done with animations');
    });
}

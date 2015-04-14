var Form = function (selector) {
    this.$el = $(selector);
}

Form.prototype = {

    getJson: function () {
        var jsonObj = {};
        var formData = this.$el.serializeArray();
        formData.forEach(function (input) {
            jsonObj[input.name] = input.value;
        });
        return jsonObj;
    },

    showErrors: function (errDict) {
        this.$el.find('.help-block').remove();
        this.$el.find('input').each(function (index, el) {
            var $el = $(el);
            if ($el.attr('name') in errDict) {
                $el.parent().addClass('has-error');
                var $help = $('<p>');
                $help.addClass('help-block');
                $help.text(errDict[$el.attr('name')]);
                $help.insertAfter($el);
            } else {
                $el.parent().removeClass('has-error');
            }
        });
    },

    hideErrors: function () {
        this.showErrors({});
    },

}

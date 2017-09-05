$.ui.djselectable.prototype._comboButtonTemplate = function (input) {
	var icon = $("<i>").addClass("icon-chevron-down");
	// Remove current classes on the text input
	$(input).attr("class", "");
	// Wrap with input-append
	$(input).wrap('<div class="input-append" />');
	// Return button link with the chosen icon
	return $("<a>").append(icon).addClass("btn btn-small");
};
$.ui.djselectable.prototype._removeButtonTemplate = function (item) {
	var icon = $("<i>").addClass("icon-remove-sign");
	// Return button link with the chosen icon
	return $("<a>").append(icon).addClass("btn btn-small pull-right");
};
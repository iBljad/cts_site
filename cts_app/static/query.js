$(document).ready(function () {
	function newParameters(query) {
		query.platform = $('#id_platform').val();
	}

	$('#id_game_0').djselectable('option', 'prepareQuery', newParameters);
});

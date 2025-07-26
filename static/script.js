$(document).ready(function() {
    if (typeof results !== 'undefined') {
        $('#results').empty();
        results.forEach(game => {
            let gameCard = `
                <div class="col-md-3">
                    <div class="game-card">
                        <a href="/game/${game.sid}" target="_blank">
                            <img src="${game.image}" alt="${game.name}" class="img-fluid">
                        </a>
                        <h5>${game.name}</h5>
                    </div>
                </div>
            `;
            $('#results').append(gameCard);
        });
    }

    $('#loadMore').on('click', function() {
        var start = $(this).data('start');
        var limit = 50;
        var query = $('#query').val();
        var match_all = $('#match_all').is(':checked');

        $.ajax({
            type: 'POST',
            url: '/load_more',
            data: {
                query: query,
                start: start,
                limit: limit,
                match_all: match_all ? 'on' : 'off'
            },
            success: function(response) {
                response.results.forEach(game => {
                    let gameCard = `
                        <div class="col-md-3">
                            <div class="game-card">
                                <a href="/game/${game.sid}" target="_blank">
                                    <img src="${game.image}" alt="${game.name}" class="img-fluid">
                                </a>
                                <h5>${game.name}</h5>
                            </div>
                        </div>
                    `;
                    $('#results').append(gameCard);
                });

                if (response.start < response.total_results) {
                    $('#loadMore').data('start', response.start);
                } else {
                    $('#loadMore').hide();
                }
            },
            error: function(error) {
                console.error("Error loading more results:", error);
            }
        });
    });

    $('#loadQueriesButton').on('click', function() {
        var lengthyQueries = [
            { query: "name == 'Portal 2'; developers == 'Valve'; platforms == 'WIN,MAC,LNX'; genres == 'Action,Adventure'; tags == 'Puzzle,Co-op,First person'", match_all: true },
            { query: "developers == 'Valve'; current_price <= 2000; platforms == 'WIN,MAC,LNX'; voiceovers == 'English'", match_all: true },
            { query: "genres == 'Action'; publishers == 'Valve'; languages == 'English,French,German'", match_all: false },
            { query: "tags == 'Puzzle'; achievements >= 50; gfq_difficulty == 'Just Right'; gfq_rating >= 4", match_all: true },
            { query: "name == 'Portal 2'; platforms == 'WIN'; meta_score >= 90; igdb_score >= 90", match_all: true }
        ];

        $('#lengthyQueries').empty();
        lengthyQueries.forEach((item, index) => {
            let queryButton = `<button class="btn btn-outline-primary query-button" data-query="${item.query}" data-match_all="${item.match_all}">Query ${index + 1}: ${item.match_all ? 'Match All' : 'Any Parameter'}</button><br><br>`;
            $('#lengthyQueries').append(queryButton);
        });

        $('#lengthyQueriesModal').modal('show');
    });

    $(document).on('click', '.query-button', function() {
        var query = $(this).data('query');
        var match_all = $(this).data('match_all');
        $('#query').val(query);
        $('#match_all').prop('checked', match_all);
        $('#lengthyQueriesModal').modal('hide');
    });
});

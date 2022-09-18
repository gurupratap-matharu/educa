const moduleOrderUrl = document
  .getElementById("moduleOrder")
  .getAttribute("data-url");

const contentOrderUrl = document
  .getElementById("contentOrder")
  .getAttribute("data-url");

$("#modules").sortable({
  stop: function (event, ui) {
    modules_order = {};
    $("#modules")
      .children()
      .each(function () {
        // update the order field
        $(this)
          .find(".order")
          .text($(this).index() + 1);
        // associate the module's id with its order
        modules_order[$(this).data("id")] = $(this).index();
      });
    $.ajax({
      type: "POST",
      url: moduleOrderUrl,
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      data: JSON.stringify(modules_order),
    });
  },
});

$("#module-contents").sortable({
  stop: function (event, ui) {
    contents_order = {};
    $("#module-contents")
      .children()
      .each(function () {
        // associate the module's id with its order
        contents_order[$(this).data("id")] = $(this).index();
      });
    $.ajax({
      type: "POST",
      url: contentOrderUrl,
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      data: JSON.stringify(contents_order),
    });
  },
});

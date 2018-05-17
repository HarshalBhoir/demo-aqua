//Simple file that change fa icon when collapsed
$(function() {
    $('.collapse_clickable').on( "click", function() {
        //This item is the <i> where the fa icon is
        $expand = $(this).find('i');
    
        if($expand.hasClass("fa fa-chevron-up")) {
            $expand.removeClass('fa fa-chevron-up').addClass('fa fa-chevron-down');
        } else if($expand.hasClass("fa fa-chevron-down")) {
            $expand.removeClass('fa fa-chevron-down').addClass('fa fa-chevron-up');
        }
    });
  });
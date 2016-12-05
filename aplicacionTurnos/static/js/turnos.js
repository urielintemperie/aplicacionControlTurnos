$('#calendarioCalendario').fullCalendar({
  height: 260,
  defaultDate: '2016-09-12',
  editable: true,
  eventLimit: true,
  dayClick: function(date, jsEvent, view) {
    alert('Clicked on: ' + date.format());
    alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
    alert('Current view: ' + view.name);
    $(this).css('background-color', 'green');
  }
});

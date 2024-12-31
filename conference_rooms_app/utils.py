from calendar import Calendar
from datetime import date
from django.urls import reverse_lazy


def my_HTMLCalendar(room, look_month, user):

    today = date.today()
    cal = Calendar().monthdatescalendar(year=look_month.year, month=look_month.month)
    cal_html = '<table class="table my-calendar">'
    cal_html += '<tr><th>Pon.</th><th>Wto.</th><th>Śro.</th><th>Czw.</th><th>Pią.</th><th>Sob.</th><th>Nie.</th></tr>'
    
    if user.is_authenticated and user.status == 2:
        for week in cal:
            cal_html += '<tr>'
            for day in week:
                if day.month == look_month.month:
                    reservation = room.reservation_set.filter(date=day).first()
                    if reservation and reservation.is_confirmed and day == today:
                        cal_html += f'''<td>
                        <a href="{reverse_lazy('admin-reservation-detail', args=[reservation.pk])}" class="my-calendar-today"
                        title="Termin Zarezerwowany"><strong>{day.day}</strong></a>
                        </td>'''
                    elif reservation and day == today:
                        cal_html += f'''<td>
                        <a href="{reverse_lazy('admin-reservation-detail', args=[reservation.pk])}" class="my-calendar-today text-danger"
                        title="Termin Zarezerwowany"><strong>{day.day}</strong></a>
                        </td>'''
                    elif reservation and reservation.is_confirmed and day > today:
                        cal_html += f'''<td>
                        <a href="{reverse_lazy('admin-reservation-detail', args=[reservation.pk])}"
                        title="Termin Zarezerwowany"><strong>{day.day}</strong></a>
                        </td>'''
                    elif reservation and day > today:
                        cal_html += f'''<td>
                        <a href="{reverse_lazy('admin-reservation-detail', args=[reservation.pk])}" class="text-danger"
                        title="Termin Zarezerwowany"><strong>{day.day}</strong></a>
                        </td>'''
                    elif reservation and day < today:
                        cal_html += f'''<td>
                        <a href="{reverse_lazy('admin-reservation-detail', args=[reservation.pk])}" 
                        title="Termin Zarezerwowany"><strong>{day.day}</strong></a>
                        </td>'''
                    elif day == today:
                        cal_html += f'<td><span class="my-calendar-today">{day.day}</span></td>'
                    else:
                        cal_html += f'<td>{day.day}</td>'
                else:
                    cal_html += '<td></td>'
            cal_html += '</tr>'
    else:
        for week in cal:
            cal_html += '<tr>'
            for day in week:
                if day.month == look_month.month:
                    if day == today and room.reservation_set.filter(date=day):
                        cal_html += f'<td><span title="Termin Zarezerwowany" class="my-calendar-today"><strong>{day.day}</strong></span></td>'
                    elif room.reservation_set.filter(date=day):
                        cal_html += f'<td><span title="Termin Zarezerwowany"><strong>{day.day}</strong></span></td>'
                    elif day == today:
                        cal_html += f'<td><span class="my-calendar-today">{day.day}</span></td>'
                    elif day < today:
                        cal_html += f'<td>{day.day}</td>'
                    else:
                        kwargs = {'room': room.pk, 'date': day}
                        cal_html += f'<td><a href="{reverse_lazy('reservation-create', kwargs=kwargs)}" title="Zarezerwuj Termin">{day.day}</a></td>'
                else:
                    cal_html += '<td></td>'
            cal_html += '</tr>'
    
    cal_html += '</table>'
    
    return cal_html
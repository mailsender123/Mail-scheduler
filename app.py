from flask import Flask, render_template, request, redirect, url_for, session

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        if "sender_email" not in session:
            session["sender_email"] = request.form["sender_email"]
            session["sender_password"] = request.form["sender_password"]
            return render_template("schedule.html")

        data = request.form
        try:
            time_parts = list(map(int, data['time'].split(':')))
            ampm = data['ampm'].lower()
            if ampm == 'pm' and time_parts[0] != 12:
                time_parts[0] += 12
            elif ampm == 'am' and time_parts[0] == 12:
                time_parts[0] = 0

            date_obj = datetime.strptime(data['date'], "%Y-%m-%d").replace(
                hour=time_parts[0], minute=time_parts[1], second=0
            )
            local_tz = ZoneInfo("Asia/Kolkata")
            date_obj = date_obj.replace(tzinfo=local_tz)

            if date_obj <= datetime.now(local_tz):
                return render_template("schedule.html", error="Choose a future time.")

            scheduler.add_job(
                send_email,
                DateTrigger(run_date=date_obj),
                args=[
                    session["sender_email"],
                    session["sender_password"],
                    data['recipient_email'],
                    data['subject'],
                    data['body']
                ],
                id=f"{session['sender_email']}_{date_obj.timestamp()}"
            )
            return redirect(url_for('success'))
        except Exception as e:
            return render_template("schedule.html", error=str(e))
    return render_template("schedule.html")

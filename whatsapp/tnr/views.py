from django.shortcuts import render
from django.http import JsonResponse
import pywhatkit as kit  # Ensure pywhatkit is installed
from datetime import datetime

def schedule_message(request):
    if request.method == "POST":
        phone = request.POST.get("phone").strip()
        message = request.POST.get("message").strip()
        time = request.POST.get("time").strip()

        # Validate phone number (India only)
        if not phone.startswith("+91") or len(phone) != 13:
            return JsonResponse({"success": False, "error": "Invalid phone number. Must be an Indian number starting with +91."})

        # Validate time
        try:
            send_hour, send_minute = map(int, time.split(":"))
            now = datetime.now()
            scheduled_time = now.replace(hour=send_hour, minute=send_minute, second=0, microsecond=0)

            if scheduled_time < now:
                return JsonResponse({"success": False, "error": "Scheduled time must be in the future."})

            # Schedule the message
            try:
                kit.sendwhatmsg(phone, message, send_hour, send_minute)
                return JsonResponse({"success": True, "message": "Message sent successfully!"})
            except Exception as e:
                return JsonResponse({"success": False, "error": f"Failed to schedule message: {str(e)}"})
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid time format. Use HH:MM in 24-hour format."})

    # Render the form for GET requests
    return render(request, "watsapp.html")

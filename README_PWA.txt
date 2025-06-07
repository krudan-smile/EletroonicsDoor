# README - Door Control App (Flet PWA)

## การใช้งานแบบ PWA

1️⃣ เพิ่ม manifest.json ใน project root
2️⃣ เพิ่ม service-worker.js ใน project root
3️⃣ ใส่ tag ใน index.html (ต้อง customize template หรือผ่าน nginx, vercel.json ฯลฯ):

<link rel="manifest" href="/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js');
  }
</script>

4️⃣ ใส่ icons ใน static/icon-192.png และ static/icon-512.png
   → ตัวอย่าง icon PNG แถมมาใน ZIP นี้

5️⃣ Deploy → User จะสามารถ Add to Home Screen ได้ → จะทำงานแบบ PWA

## หมายเหตุ

- main.py → ให้ใช้ version ล่าสุดที่แก้แล้ว (Token + Responsive + Internet Status + Card Center)
- Flet ยังไม่ generate PWA auto → เราต้องใส่เอง
- service worker ที่แถมเป็นแบบ Basic (สามารถเขียนให้ advanced ได้ เช่น version cache)

## วิธี build / deploy

- สามารถ deploy บน Render / Vercel / Netlify / Cloudflare Pages ได้
- ต้องแน่ใจว่า server serve manifest.json และ service-worker.js แบบ public

Good luck 🚀
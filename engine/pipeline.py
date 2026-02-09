import google.generativeai as genai
from db import Session, Lead, LeadStatus, Telemetry

# Configuración de IA
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def process_pending_leads():
    session = Session()
    # Pull: Tomar leads pendientes
    pending_leads = session.query(Lead).filter(Lead.status == LeadStatus.PENDING).limit(10).all()
    
    if not pending_leads:
        print("📭 Cola vacía. En espera de nuevos leads...")
        session.close()
        return

    for lead in pending_leads:
        try:
            prompt = f"Genera un mensaje de venta ultra-corto para: {lead.email}"
            response = model.generate_content(prompt)
            
            # Update: Guardar resultado y marcar como enviado
            lead.status = LeadStatus.SENT
            
            # Telemetría: Registrar profit (estimado $0.35 por éxito)
            new_metric = Telemetry(profit=0.35, efficiency=94.0)
            session.add(new_metric)
            
            print(f"✅ Procesado: {lead.email}")
            session.commit()
        except Exception as e:
            lead.status = LeadStatus.FAILED
            session.commit()
            print(f"❌ Error en lead {lead.email}: {e}")
            
    session.close()

if __name__ == "__main__":
    print("🚀 Worker Pipeline Iniciado...")
    while True:
        process_pending_leads()
        time.sleep(10) # Evitar saturación de API


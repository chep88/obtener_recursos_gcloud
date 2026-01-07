import os
from google.cloud import compute_v1
from typing import List

class GCPResourceAuditor:
    def __init__(self, project_id):
        self.project_id = project_id
        # El cliente detectará automáticamente las credenciales de gcloud auth
        self.instance_client = compute_v1.InstancesClient()

    def list_instances(self, zone: str = "us-central1-a") -> List[dict]:
        """
        Lista todas las instancias en una zona específica y su estado.
        """
        print(f"🔍 Buscando recursos en proyecto: {self.project_id}, Zona: {zone}...")
        results = []
        
        try:
            request = compute_v1.ListInstancesRequest(
                project=self.project_id,
                zone=zone
            )
            for instance in self.instance_client.list(request=request):
                results.append({
                    "name": instance.name,
                    "status": instance.status,
                    "machine_type": instance.machine_type.split('/')[-1],
                    "network_ip": instance.network_interfaces[0].network_i_p
                })
                
            return results
        except Exception as e:
            print(f"❌ Error obteniendo instancias: {e}")
            return []

if __name__ == "__main__":
    # Ejemplo de uso
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "tu-proyecto-aqui")
    
    auditor = GCPResourceAuditor(PROJECT_ID)
    instances = auditor.list_instances()
    
    print("\n📊 Reporte de Instancias:")
    for inst in instances:
        print(f"- [{inst['status']}] {inst['name']} ({inst['network_ip']})")

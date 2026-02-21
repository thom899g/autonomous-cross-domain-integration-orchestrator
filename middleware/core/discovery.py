import logging
from typing import Dict, Any
from ..utils.connector import ServiceConnector

class DiscoveryAgent:
    def __init__(self):
        self.connector = ServiceConnector()
        self.service_map: Dict[str, str] = {}

    def discover_services(self) -> Dict[str, str]:
        """Discover and map services across domains."""
        try:
            services = self.connector.query("GET", "http://service-discovery/api/services")
            if not services:
                logging.warning("No services discovered.")
                return {}
            
            # Map service names to endpoints
            for service in services:
                self.service_map[service['name']] = service['endpoint']
            
            return self.service_map
        except Exception as e:
            logging.error(f"Discovery failed: {str(e)}")
            raise

    def get_service_endpoint(self, service_name: str) -> str:
        """Retrieve endpoint for a specific service."""
        if service_name in self.service_map:
            return self.service_map[service_name]
        else:
            raise ValueError(f"Service {service_name} not found.")
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Feature:
    name: str
    description: str

@dataclass
class Product:
    name: str
    description: str
    features: List[Feature]
    metrics: Optional[Dict[str, str]] = None
    benefits: Optional[List[str]] = None
    use_cases: Optional[List[str]] = None

@dataclass
class Industry:
    name: str
    description: str
    use_cases: Optional[List[str]] = None
    challenges: Optional[List[str]] = None
    solutions: Optional[List[str]] = None

class ElasticRunKnowledgeBase:
    def __init__(self):
        self.products = [
            Product(
                name="Libera",
                description="A comprehensive logistics management platform",
                features=[
                    Feature(
                        name="Route Optimization",
                        description="AI-powered route optimization for efficient deliveries"
                    ),
                    Feature(
                        name="Real-time Tracking",
                        description="Live tracking of all shipments and delivery personnel"
                    )
                ],
                benefits=[
                    "Reduced delivery costs",
                    "Improved customer satisfaction",
                    "Enhanced operational efficiency"
                ],
                use_cases=[
                    "Last-mile delivery optimization",
                    "Fleet management",
                    "Delivery scheduling"
                ]
            ),
            Product(
                name="RTMNxt",
                description="Route-to-market solution for FMCG companies",
                features=[
                    Feature(
                        name="Market Coverage",
                        description="Expand market reach through data-driven insights"
                    ),
                    Feature(
                        name="Sales Analytics",
                        description="Advanced analytics for sales performance optimization"
                    )
                ],
                benefits=[
                    "Increased market penetration",
                    "Better sales efficiency",
                    "Data-driven decision making"
                ],
                use_cases=[
                    "FMCG distribution",
                    "Sales force automation",
                    "Market expansion"
                ]
            ),
            Product(
                name="Mity",
                description="AI-Powered Identity and Face Recognition Software for secure workforce verification",
                features=[
                    Feature(
                        name="AI-Powered Identity Verification",
                        description="Real-time identity verification with liveness detection and selfie verification"
                    ),
                    Feature(
                        name="Face Recognition",
                        description="Advanced face recognition that works with masks, helmets, and varying conditions"
                    ),
                    Feature(
                        name="Fraud Prevention",
                        description="AI-driven risk prevention engine to block impersonation attempts and duplicate registrations"
                    ),
                    Feature(
                        name="Real-time Monitoring",
                        description="Instant alerts and AI-powered monitoring to prevent fraudulent activities"
                    )
                ],
                benefits=[
                    "99.97% accuracy score",
                    "Verifies over 6 million identities monthly",
                    "20% increase in CSAT score",
                    "No extra hardware required - works with standard cameras",
                    "Enterprise-grade protection without excessive costs"
                ],
                use_cases=[
                    "Workforce identity verification",
                    "Secure onboarding",
                    "Access control",
                    "Fraud prevention"
                ]
            ),
            Product(
                name="Velocity",
                description="Last-mile delivery optimization platform",
                features=[
                    Feature(
                        name="Dynamic Routing",
                        description="Real-time dynamic routing for last-mile deliveries"
                    ),
                    Feature(
                        name="Delivery Tracking",
                        description="End-to-end delivery tracking and monitoring"
                    )
                ],
                benefits=[
                    "Faster deliveries",
                    "Lower operational costs",
                    "Better customer experience"
                ],
                use_cases=[
                    "Last-mile delivery",
                    "E-commerce fulfillment",
                    "Hyperlocal delivery"
                ]
            ),
            Product(
                name="Daakia",
                description="Intelligent Address Sorting Engine",
                features=[
                    Feature(
                        name="Address Verification",
                        description="AI-powered address verification and standardization"
                    ),
                    Feature(
                        name="Geocoding",
                        description="Accurate geocoding and location intelligence"
                    )
                ],
                benefits=[
                    "Reduced failed deliveries",
                    "Improved address accuracy",
                    "Enhanced delivery success rate"
                ],
                use_cases=[
                    "Address verification",
                    "Location intelligence",
                    "Delivery optimization"
                ]
            )
        ]
        
        self.industries = [
            Industry(
                name="E-commerce",
                description="Digital retail and online marketplace solutions",
                use_cases=[
                    "Last-mile delivery",
                    "Inventory management",
                    "Order fulfillment"
                ],
                challenges=[
                    "High delivery costs",
                    "Meeting delivery timelines",
                    "Managing returns"
                ],
                solutions=[
                    "Optimized delivery routes",
                    "Real-time tracking",
                    "Automated dispatch"
                ]
            ),
            Industry(
                name="FMCG",
                description="Fast-moving consumer goods distribution",
                use_cases=[
                    "Distribution network optimization",
                    "Sales force management",
                    "Market penetration"
                ],
                challenges=[
                    "Market coverage",
                    "Stock management",
                    "Sales efficiency"
                ],
                solutions=[
                    "Data-driven market insights",
                    "Sales force automation",
                    "Real-time inventory tracking"
                ]
            )
        ]

    def get_all_products(self) -> List[Product]:
        return self.products

    def get_all_industries(self) -> List[Industry]:
        return self.industries

    def get_product_by_name(self, name: str) -> Optional[Product]:
        return next((p for p in self.products if p.name.lower() == name.lower()), None)

    def get_industry_by_name(self, name: str) -> Optional[Industry]:
        return next((i for i in self.industries if i.name.lower() == name.lower()), None)

    def search(self, query: str) -> Dict:
        """Search the knowledge base for relevant information."""
        query = query.lower()
        results = {
            'products': [],
            'industries': [],
            'features': [],
            'benefits': [],
            'use_cases': [],
            'solutions': []
        }

        # Search products
        for product in self.products:
            if query in product.name.lower() or query in product.description.lower():
                results['products'].append((product.name, product.description))
            
            # Search features
            for feature in product.features:
                if query in feature.name.lower() or query in feature.description.lower():
                    results['features'].append((product.name, feature.name, feature.description))
            
            # Search benefits
            if product.benefits:
                for benefit in product.benefits:
                    if query in benefit.lower():
                        results['benefits'].append((product.name, benefit))
            
            # Search use cases
            if product.use_cases:
                for use_case in product.use_cases:
                    if query in use_case.lower():
                        results['use_cases'].append((product.name, use_case))

        # Search industries
        for industry in self.industries:
            if query in industry.name.lower() or query in industry.description.lower():
                results['industries'].append((industry.name, industry.description))
            
            # Search use cases
            if industry.use_cases:
                for use_case in industry.use_cases:
                    if query in use_case.lower():
                        results['use_cases'].append((industry.name, use_case))
            
            # Search challenges
            if industry.challenges:
                for challenge in industry.challenges:
                    if query in challenge.lower():
                        results['challenges'].append((industry.name, challenge))
            
            # Search solutions
            if industry.solutions:
                for solution in industry.solutions:
                    if query in solution.lower():
                        results['solutions'].append((industry.name, solution))

        return results 
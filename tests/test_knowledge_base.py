from knowledge_base.elasticrun_kb import ElasticRunKnowledgeBase

def test_knowledge_base():
    kb = ElasticRunKnowledgeBase()
    
    # Test products
    products = kb.get_all_products()
    assert len(products) == 2
    assert products[0].name == "Libera"
    assert products[1].name == "RTMNxt"
    
    # Test product features
    libera = kb.get_product_by_name("Libera")
    assert libera is not None
    assert len(libera.features) == 7
    assert libera.metrics["Shipments Handled"] == "2 Bn+"
    
    # Test industries
    industries = kb.get_all_industries()
    assert len(industries) == 4
    assert industries[0].name == "E-Commerce"
    
    # Test industry use cases
    ecommerce = kb.get_industry_by_name("E-Commerce")
    assert ecommerce is not None
    assert len(ecommerce.use_cases) == 4
    assert "Last-mile delivery optimization" in ecommerce.use_cases

if __name__ == "__main__":
    test_knowledge_base()
    print("All tests passed!") 
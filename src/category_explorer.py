"""
Utility script to explore arXiv categories and extract them from papers.
"""

import arxiv
from typing import List, Dict

def get_paper_categories(paper_id: str) -> List[str]:
    """
    Get the categories of a specific paper.
    
    Args:
        paper_id: arXiv ID (e.g., "2406.01234")
    
    Returns:
        List of category codes (e.g., ["cs.CL", "cs.AI"])
    """
    search = arxiv.Search(id_list=[paper_id])
    results = list(search.results())
    
    if results:
        paper = results[0]
        return paper.categories
    else:
        return []

def search_by_category(category: str, max_results: int = 10) -> List[Dict]:
    """
    Search for papers in a specific category.
    
    Args:
        category: Category code (e.g., "cs.CL")
        max_results: Maximum number of results
    
    Returns:
        List of paper information dictionaries
    """
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    for paper in search.results():
        papers.append({
            'id': paper.entry_id,
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'categories': paper.categories,
            'published': paper.published.isoformat(),
            'summary': paper.summary[:200] + "..." if len(paper.summary) > 200 else paper.summary
        })
    
    return papers

def get_common_categories() -> Dict[str, str]:
    """
    Get a dictionary of common arXiv categories with descriptions.
    """
    return {
        # Computer Science
        "cs.AI": "Artificial Intelligence",
        "cs.CL": "Computation and Language (NLP)",
        "cs.CV": "Computer Vision and Pattern Recognition", 
        "cs.LG": "Machine Learning",
        "cs.NE": "Neural and Evolutionary Computing",
        "cs.IR": "Information Retrieval",
        "cs.SE": "Software Engineering",
        "cs.DC": "Distributed, Parallel, and Cluster Computing",
        "cs.CR": "Cryptography and Security",
        "cs.DB": "Databases",
        "cs.AR": "Hardware Architecture",
        "cs.CG": "Computational Geometry",
        "cs.GT": "Computer Science and Game Theory",
        "cs.LO": "Logic in Computer Science",
        "cs.MS": "Mathematical Software",
        "cs.NA": "Numerical Analysis",
        "cs.OS": "Operating Systems",
        "cs.PF": "Performance",
        "cs.PL": "Programming Languages",
        "cs.RO": "Robotics",
        "cs.SC": "Symbolic Computation",
        "cs.SD": "Sound",
        "cs.SI": "Social and Information Networks",
        "cs.SY": "Systems and Control",
        
        # Mathematics
        "math.OC": "Optimization and Control",
        "math.ST": "Statistics Theory",
        "math.NA": "Numerical Analysis",
        "math.PR": "Probability",
        "math.AT": "Algebraic Topology",
        "math.AG": "Algebraic Geometry",
        "math.AP": "Analysis of PDEs",
        "math.CT": "Category Theory",
        "math.CA": "Classical Analysis and ODEs",
        "math.CO": "Combinatorics",
        "math.AC": "Commutative Algebra",
        "math.CV": "Complex Variables",
        "math.DG": "Differential Geometry",
        "math.DS": "Dynamical Systems",
        "math.FA": "Functional Analysis",
        "math.GM": "General Mathematics",
        "math.GN": "General Topology",
        "math.GT": "Geometric Topology",
        "math.GR": "Group Theory",
        "math.HO": "History and Overview",
        "math.IT": "Information Theory",
        "math.KT": "K-Theory and Homology",
        "math.LO": "Logic",
        "math.MP": "Mathematical Physics",
        "math.MG": "Metric Geometry",
        "math.NT": "Number Theory",
        "math.OA": "Operator Algebras",
        "math.RA": "Rings and Algebras",
        "math.RT": "Representation Theory",
        "math.SP": "Spectral Theory",
        "math.SG": "Symplectic Geometry",
        
        # Physics
        "physics.comp-ph": "Computational Physics",
        "physics.data-an": "Data Analysis, Statistics and Probability",
        "physics.acc-ph": "Accelerator Physics",
        "physics.ao-ph": "Atmospheric and Oceanic Physics",
        "physics.app-ph": "Applied Physics",
        "physics.atm-clus": "Atomic and Molecular Clusters",
        "physics.atom-ph": "Atomic Physics",
        "physics.bio-ph": "Biological Physics",
        "physics.chem-ph": "Chemical Physics",
        "physics.class-ph": "Classical Physics",
        "physics.flu-dyn": "Fluid Dynamics",
        "physics.gen-ph": "General Physics",
        "physics.geo-ph": "Geophysics",
        "physics.hist-ph": "History and Philosophy of Physics",
        "physics.ins-det": "Instrumentation and Detectors",
        "physics.med-ph": "Medical Physics",
        "physics.optics": "Optics",
        "physics.plasm-ph": "Plasma Physics",
        "physics.pop-ph": "Popular Physics",
        "physics.soc-ph": "Physics and Society",
        "physics.space-ph": "Space Physics",
        
        # Quantitative Biology
        "q-bio.BM": "Biomolecules",
        "q-bio.CB": "Cell Behavior",
        "q-bio.GN": "Genomics",
        "q-bio.MN": "Molecular Networks",
        "q-bio.NC": "Neurons and Cognition",
        "q-bio.OT": "Other Quantitative Biology",
        "q-bio.PE": "Populations and Evolution",
        "q-bio.QM": "Quantitative Methods",
        "q-bio.SC": "Subcellular Processes",
        "q-bio.TO": "Tissues and Organs"
    }

# Example usage
if __name__ == "__main__":
    # Example 1: Get categories of a specific paper
    paper_id = "2406.01234"
    categories = get_paper_categories(paper_id)
    print(f"Categories for {paper_id}: {categories}")
    
    # Example 2: Search papers in a category
    category = "cs.CL"
    papers = search_by_category(category, max_results=3)
    print(f"\nRecent papers in {category}:")
    for paper in papers:
        print(f"- {paper['title']}")
        print(f"  Categories: {paper['categories']}")
        print()
    
    # Example 3: Show common categories
    common_cats = get_common_categories()
    print("Common arXiv Categories:")
    for code, description in list(common_cats.items())[:10]:  # Show first 10
        print(f"{code}: {description}") 
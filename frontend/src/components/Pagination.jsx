export default function Pagination({ page, total, parPage, onChange }) {
    const pages = Math.max(1, Math.ceil(total / parPage));
    if (pages <= 1) return null;
  
    return (
      <div className="pagination">
        <button className="btn-sec" disabled={page <= 1} onClick={() => onChange(page - 1)}>
          Précédent
        </button>
        <span>Page {page} sur {pages}</span>
        <button className="btn-sec" disabled={page >= pages} onClick={() => onChange(page + 1)}>
          Suivant
        </button>
      </div>
    );
  }
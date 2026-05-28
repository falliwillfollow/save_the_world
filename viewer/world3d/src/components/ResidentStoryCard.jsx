export default function ResidentStoryCard({ archetypes, selectedId, onSelect }) {
  const selected = archetypes.find(archetype => archetype.id === selectedId) || archetypes[0];
  if (!selected) return null;

  return (
    <section className="abundance-section resident-story-card">
      <h2>Resident Archetype</h2>
      <div className="resident-selector">
        {archetypes.map(archetype => (
          <button
            key={archetype.id}
            type="button"
            className={selected.id === archetype.id ? "is-active" : ""}
            onClick={() => onSelect(archetype.id)}
          >
            {archetype.label}
          </button>
        ))}
      </div>
      <article>
        <strong>{selected.label}</strong>
        <span>{selected.archetype}</span>
        <p>{selected.civic_floor_life?.description}</p>
        <ul>
          {(selected.narrative_beats || []).map((beat, index) => (
            <li key={`${beat.time}-${index}`}>{beat.time}: {beat.text}</li>
          ))}
        </ul>
      </article>
    </section>
  );
}

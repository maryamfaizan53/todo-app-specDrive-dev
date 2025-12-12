/**
 * Filters component for todo list
 */
'use client';

export default function TodoFilters({ filters, onFilterChange }) {
  const handleSearchChange = (e) => {
    onFilterChange({ ...filters, search: e.target.value });
  };

  const handleCompletedFilter = (value) => {
    onFilterChange({ ...filters, completed: value });
  };

  const handleSortChange = (e) => {
    onFilterChange({ ...filters, sort: e.target.value });
  };

  const clearFilters = () => {
    onFilterChange({
      completed: 'all',
      search: '',
      sort: 'created_at',
      order: 'desc'
    });
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 space-y-3">
      <div className="flex flex-col md:flex-row gap-3">
        <input
          type="text"
          placeholder="Search tasks..."
          value={filters.search}
          onChange={handleSearchChange}
          className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <div className="flex gap-2">
          <button
            onClick={() => handleCompletedFilter('all')}
            className={`px-3 py-2 rounded transition ${
              filters.completed === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All
          </button>
          <button
            onClick={() => handleCompletedFilter('false')}
            className={`px-3 py-2 rounded transition ${
              filters.completed === 'false'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Active
          </button>
          <button
            onClick={() => handleCompletedFilter('true')}
            className={`px-3 py-2 rounded transition ${
              filters.completed === 'true'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Done
          </button>
        </div>
      </div>

      <div className="flex justify-between items-center">
        <select
          value={filters.sort}
          onChange={handleSortChange}
          className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="created_at">Created Date</option>
          <option value="updated_at">Updated Date</option>
          <option value="title">Title</option>
        </select>

        <button
          onClick={clearFilters}
          className="px-3 py-2 text-sm text-blue-600 hover:text-blue-800 transition"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
}

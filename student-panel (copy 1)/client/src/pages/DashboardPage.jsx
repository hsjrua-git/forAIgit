import { useCallback, useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router';
import { getTrends } from '../api/dashboard.js';
import { getResults } from '../api/results.js';
import { useAuth } from '../auth/AuthContext.jsx';
import GroupFilter from '../components/GroupFilter.jsx';
import CompletionHub from '../components/CompletionHub.jsx';
import EmptyState from '../components/EmptyState.jsx';
import ParameterDrawer from '../components/ParameterDrawer.jsx';
import PeriodPicker from '../components/PeriodPicker.jsx';
import UnmeasuredList from '../components/UnmeasuredList.jsx';
import {
  cohortField,
  parameterStats,
  summarize,
  trendSeries,
  unmeasuredStudents,
} from '../lib/dashboard.js';
import { formatIsoDate } from '../lib/format.js';
import { usePeriods } from '../lib/usePeriods.js';

function DashboardPage() {
  const { can } = useAuth();
  const periodsQuery = usePeriods();
  const periods = periodsQuery.data;
  const [chosen, setChosen] = useState(null);
  const [groupId, setGroupId] = useState('');
  const periodNumber = chosen ?? periods?.current ?? null;

  const resultsQuery = useQuery({
    queryKey: ['results', periodNumber, groupId],
    queryFn: () => getResults(periodNumber, groupId || null),
    enabled: periodNumber !== null,
  });
  const trendsQuery = useQuery({
    queryKey: ['trends', groupId],
    queryFn: () => getTrends(groupId || null),
  });

  const results = resultsQuery.data;
  const summary = useMemo(() => (results ? summarize(results) : null), [results]);
  const cohort = useMemo(() => (results ? cohortField(results) : []), [results]);
  const stats = useMemo(() => (results ? parameterStats(results) : []), [results]);
  const unmeasured = useMemo(
    () => (results ? unmeasuredStudents(results) : []),
    [results]
  );
  // Which parameter's detail drawer is open (its id), or null. The drawer is
  // always mounted so both its slide-in and slide-out come from CSS; closing
  // just clears the id and the panel keeps its last content until off-screen.
  const [openParamId, setOpenParamId] = useState(null);
  const closeDrawer = useCallback(() => setOpenParamId(null), []);

  if (periodsQuery.isPending) {
    return (
      <main aria-busy="true">
        <div className="page-loading" role="status" aria-live="polite">
          <span className="spinner" aria-hidden="true" />
          <p>Loading…</p>
        </div>
      </main>
    );
  }
  if (periodsQuery.isError) {
    return (
      <main>
        <EmptyState
          tone="danger"
          title="Couldn't load the dashboard"
          description={periodsQuery.error.message}
        />
      </main>
    );
  }
  if (!periods.anchorDate) {
    return (
      <main>
        <h1>Dashboard</h1>
        {can('settings.manage') ? (
          <EmptyState
            title="Set up the calendar"
            description="Set the period start date to begin tracking scores."
          >
            <p>
              <Link to="/settings">Go to Settings</Link>
            </p>
          </EmptyState>
        ) : (
          <EmptyState
            title="Not set up yet"
            description="An administrator needs to set the period start date first."
          />
        )}
      </main>
    );
  }
  if (periods.current === null) {
    return (
      <main>
        <h1>Dashboard</h1>
        <EmptyState
          title="Period 1 hasn't started"
          description="Once the first period begins, results will show up here."
        />
      </main>
    );
  }

  const upToSelected = periods.periods.filter(
    (period) => period.number <= periodNumber
  );

  // The parameter whose drawer is open, and its trend line up to the selected
  // period. Stats default to [] so the lookup is safe before results land; trend
  // is only computed when a parameter is actually selected.
  const openStat =
    openParamId !== null
      ? stats.find((stat) => stat.parameter.id === openParamId) ?? null
      : null;
  const openTrend = openStat
    ? trendSeries({
        trends: trendsQuery.data ?? [],
        periods: upToSelected,
        parameterId: openParamId,
      })
    : [];

  return (
    <main className="wide">
      <div className="page-head">
        <h1>Dashboard</h1>
        {can('scores.enter') && periodNumber === periods.current && (
          <div className="page-head-actions">
            <Link className="btn primary" to="/evaluate">
              Enter scores
            </Link>
          </div>
        )}
      </div>

      <div className="toolbar">
        <PeriodPicker
          periods={periods}
          value={periodNumber}
          onChange={setChosen}
        />
        <GroupFilter value={groupId} onChange={setGroupId} />
      </div>

      {resultsQuery.isPending && <p className="hint">Loading…</p>}
      {resultsQuery.isError && (
        <p className="error">{resultsQuery.error.message}</p>
      )}

      {results && (
        <>
          <p className="summary-line">
            Period {results.periodNumber} ({formatIsoDate(results.startDate)} –{' '}
            {formatIsoDate(results.endDate)})
          </p>
          {results.truncated && (
            <p className="hint">
              Only the first {results.students.length} of {results.total}{' '}
              students are included.
            </p>
          )}

          {results.students.length === 0 ? (
            <EmptyState
              title="No students yet"
              description="Add students to start entering and reviewing scores."
            >
              {can('students.create') && (
                <p>
                  <Link to="/students">Go to Students</Link>
                </p>
              )}
            </EmptyState>
          ) : results.parameters.length === 0 ? (
            <EmptyState
              title="Nothing measured this period"
              description="No parameters were used in this period, and no scores were entered yet."
            />
          ) : (
            <>
              <CompletionHub
                summary={summary}
                field={cohort}
                stats={stats}
                onSelectParameter={setOpenParamId}
              />

              <section>
                <h2>Needs scoring</h2>
                <UnmeasuredList items={unmeasured} />
              </section>
            </>
          )}
        </>
      )}

      <ParameterDrawer
        open={Boolean(openStat)}
        stat={openStat}
        trend={openTrend}
        trendError={trendsQuery.isError ? trendsQuery.error.message : null}
        onClose={closeDrawer}
      />
    </main>
  );
}

export default DashboardPage;
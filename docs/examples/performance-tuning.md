# ⚡ Performance Tuning Examples

Beispiele für Performance-Optimierung und Tuning von Keiko Personal Assistant.

## 🚀 Database Performance

### Connection Pooling Optimization

```python
# config/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import QueuePool

# Optimierte Database-Konfiguration
DATABASE_CONFIG = {
    "pool_size": 20,           # Basis-Pool-Größe
    "max_overflow": 30,        # Zusätzliche Verbindungen bei Bedarf
    "pool_timeout": 30,        # Timeout für Pool-Verbindung
    "pool_recycle": 3600,      # Verbindungen nach 1h recyceln
    "pool_pre_ping": True,     # Verbindungen vor Nutzung testen
    "echo": False,             # SQL-Logging deaktivieren in Produktion
    "future": True
}

# Engine mit optimierten Einstellungen
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/keiko",
    poolclass=QueuePool,
    **DATABASE_CONFIG
)

# Session-Factory
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False  # Manuelles Flushing für bessere Kontrolle
)

# Optimierte Repository-Implementierung
class OptimizedAgentRepository:
    """Performance-optimiertes Agent-Repository."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_agents_batch(self, agent_ids: List[str]) -> List[Agent]:
        """Lädt mehrere Agenten in einem Query."""

        async with self.session_factory() as session:
            # Batch-Loading mit IN-Clause
            query = select(AgentModel).where(AgentModel.id.in_(agent_ids))
            result = await session.execute(query)
            agent_models = result.scalars().all()

            return [Agent.from_model(model) for model in agent_models]

    async def get_agents_with_stats(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Lädt Agenten mit Statistiken in einem Query."""

        async with self.session_factory() as session:
            # JOIN-Query für bessere Performance
            query = (
                select(
                    AgentModel.id,
                    AgentModel.name,
                    AgentModel.type,
                    func.count(TaskModel.id).label('task_count'),
                    func.avg(TaskModel.duration).label('avg_duration')
                )
                .outerjoin(TaskModel, AgentModel.id == TaskModel.agent_id)
                .group_by(AgentModel.id, AgentModel.name, AgentModel.type)
                .limit(limit)
            )

            result = await session.execute(query)
            return [dict(row) for row in result]

    async def bulk_update_status(self, updates: List[Dict[str, Any]]) -> None:
        """Bulk-Update für bessere Performance."""

        async with self.session_factory() as session:
            # Bulk-Update mit bulk_update_mappings
            await session.execute(
                update(AgentModel),
                updates
            )
            await session.commit()
```

### Query Optimization

```python
# Optimierte Queries mit Eager Loading
class OptimizedTaskService:
    """Performance-optimierter Task-Service."""

    async def get_tasks_with_relations(self, user_id: str) -> List[Dict[str, Any]]:
        """Lädt Tasks mit allen Relationen in einem Query."""

        async with self.session_factory() as session:
            # Eager Loading mit joinedload
            query = (
                select(TaskModel)
                .options(
                    joinedload(TaskModel.agent),
                    joinedload(TaskModel.user),
                    joinedload(TaskModel.results)
                )
                .where(TaskModel.user_id == user_id)
                .order_by(TaskModel.created_at.desc())
            )

            result = await session.execute(query)
            tasks = result.unique().scalars().all()

            return [self._task_to_dict(task) for task in tasks]

    async def get_task_statistics(self, date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Berechnet Task-Statistiken mit optimierten Aggregationen."""

        async with self.session_factory() as session:
            # Aggregation-Query
            query = (
                select(
                    TaskModel.status,
                    TaskModel.type,
                    func.count().label('count'),
                    func.avg(TaskModel.duration).label('avg_duration'),
                    func.min(TaskModel.duration).label('min_duration'),
                    func.max(TaskModel.duration).label('max_duration')
                )
                .where(
                    TaskModel.created_at.between(date_range[0], date_range[1])
                )
                .group_by(TaskModel.status, TaskModel.type)
            )

            result = await session.execute(query)

            statistics = {}
            for row in result:
                key = f"{row.status}_{row.type}"
                statistics[key] = {
                    'count': row.count,
                    'avg_duration': float(row.avg_duration or 0),
                    'min_duration': float(row.min_duration or 0),
                    'max_duration': float(row.max_duration or 0)
                }

            return statistics

# Database-Indizes für bessere Performance
"""
-- Wichtige Indizes für Performance
CREATE INDEX CONCURRENTLY idx_tasks_user_created
ON tasks(user_id, created_at DESC);

CREATE INDEX CONCURRENTLY idx_tasks_status_type
ON tasks(status, type);

CREATE INDEX CONCURRENTLY idx_tasks_agent_status
ON tasks(agent_id, status)
WHERE status IN ('running', 'pending');

CREATE INDEX CONCURRENTLY idx_agents_type_status
ON agents(type, status);

-- Partial Index für aktive Tasks
CREATE INDEX CONCURRENTLY idx_tasks_active
ON tasks(created_at DESC)
WHERE status IN ('running', 'pending');
"""
```

## 🔄 Async Performance

### Optimized Async Processing

```python
import asyncio
from asyncio import Semaphore, Queue
from typing import List, Callable, Any

class AsyncTaskProcessor:
    """Hochperformanter asynchroner Task-Processor."""

    def __init__(self, max_concurrent: int = 100, queue_size: int = 1000):
        self.max_concurrent = max_concurrent
        self.semaphore = Semaphore(max_concurrent)
        self.task_queue = Queue(maxsize=queue_size)
        self.workers = []
        self.running = False

    async def start(self, num_workers: int = 10):
        """Startet Worker-Pool."""
        self.running = True

        for i in range(num_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)

    async def stop(self):
        """Stoppt Worker-Pool."""
        self.running = False

        # Alle Worker beenden
        for worker in self.workers:
            worker.cancel()

        await asyncio.gather(*self.workers, return_exceptions=True)

    async def submit_task(self, coro: Callable, *args, **kwargs) -> asyncio.Future:
        """Fügt Task zur Queue hinzu."""
        future = asyncio.Future()

        await self.task_queue.put({
            'coro': coro,
            'args': args,
            'kwargs': kwargs,
            'future': future
        })

        return future

    async def _worker(self, worker_id: str):
        """Worker-Loop."""
        while self.running:
            try:
                # Task aus Queue holen
                task_item = await asyncio.wait_for(
                    self.task_queue.get(),
                    timeout=1.0
                )

                # Task mit Semaphore ausführen
                async with self.semaphore:
                    try:
                        result = await task_item['coro'](
                            *task_item['args'],
                            **task_item['kwargs']
                        )
                        task_item['future'].set_result(result)
                    except Exception as e:
                        task_item['future'].set_exception(e)

                self.task_queue.task_done()

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")

# Batch-Processing für bessere Performance
class BatchProcessor:
    """Batch-Processor für effiziente Verarbeitung."""

    def __init__(self, batch_size: int = 100, flush_interval: float = 5.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.batch = []
        self.last_flush = time.time()
        self.processors = {}

    async def add_item(self, processor_name: str, item: Any):
        """Fügt Item zum Batch hinzu."""
        if processor_name not in self.batch:
            self.batch[processor_name] = []

        self.batch[processor_name].append(item)

        # Batch verarbeiten wenn voll oder Timeout erreicht
        if (len(self.batch[processor_name]) >= self.batch_size or
            time.time() - self.last_flush > self.flush_interval):
            await self._flush_batch(processor_name)

    async def _flush_batch(self, processor_name: str):
        """Verarbeitet Batch."""
        if processor_name not in self.batch or not self.batch[processor_name]:
            return

        items = self.batch[processor_name]
        self.batch[processor_name] = []
        self.last_flush = time.time()

        # Batch-Processor ausführen
        if processor_name in self.processors:
            await self.processors[processor_name](items)

    def register_processor(self, name: str, processor: Callable):
        """Registriert Batch-Processor."""
        self.processors[name] = processor

# Verwendung für Agent-Task-Verarbeitung
class HighPerformanceAgentService:
    """High-Performance Agent-Service."""

    def __init__(self):
        self.task_processor = AsyncTaskProcessor(max_concurrent=50)
        self.batch_processor = BatchProcessor(batch_size=50)

        # Batch-Processors registrieren
        self.batch_processor.register_processor(
            "task_results",
            self._process_task_results_batch
        )
        self.batch_processor.register_processor(
            "metrics",
            self._process_metrics_batch
        )

    async def execute_tasks_parallel(self, tasks: List[Task]) -> List[TaskResult]:
        """Führt Tasks parallel aus."""

        # Tasks in Gruppen aufteilen
        task_groups = [tasks[i:i+10] for i in range(0, len(tasks), 10)]

        # Gruppen parallel verarbeiten
        results = []
        for group in task_groups:
            group_results = await asyncio.gather(*[
                self.task_processor.submit_task(self._execute_single_task, task)
                for task in group
            ])
            results.extend(group_results)

        return results

    async def _execute_single_task(self, task: Task) -> TaskResult:
        """Führt einzelne Task aus."""
        start_time = time.time()

        try:
            # Task-Ausführung
            result = await self._perform_task_execution(task)

            # Ergebnis zum Batch hinzufügen
            await self.batch_processor.add_item("task_results", {
                'task_id': task.id,
                'result': result,
                'duration': time.time() - start_time
            })

            return result

        except Exception as e:
            # Fehler-Metrik zum Batch hinzufügen
            await self.batch_processor.add_item("metrics", {
                'type': 'task_error',
                'task_id': task.id,
                'error': str(e)
            })
            raise

    async def _process_task_results_batch(self, results: List[Dict[str, Any]]):
        """Verarbeitet Task-Ergebnisse im Batch."""

        # Bulk-Insert in Database
        async with self.session_factory() as session:
            result_models = [
                TaskResultModel(
                    task_id=item['task_id'],
                    result_data=item['result'],
                    duration=item['duration']
                )
                for item in results
            ]

            session.add_all(result_models)
            await session.commit()

    async def _process_metrics_batch(self, metrics: List[Dict[str, Any]]):
        """Verarbeitet Metriken im Batch."""

        for metric in metrics:
            if metric['type'] == 'task_error':
                TASK_ERRORS_COUNTER.labels(
                    task_id=metric['task_id']
                ).inc()
```

## 🗄️ Caching Strategies

### Multi-Level Caching

```python
from typing import Optional, Any, Union
import pickle
import json
import hashlib

class MultiLevelCache:
    """Multi-Level-Cache mit Memory, Redis und Database."""

    def __init__(self, redis_client, db_session_factory):
        self.memory_cache = {}  # L1 Cache
        self.redis_client = redis_client  # L2 Cache
        self.db_session_factory = db_session_factory  # L3 Cache

        # Cache-Konfiguration
        self.memory_ttl = 300  # 5 Minuten
        self.redis_ttl = 3600  # 1 Stunde
        self.db_ttl = 86400    # 24 Stunden

        self.memory_max_size = 1000

    async def get(self, key: str) -> Optional[Any]:
        """Ruft Wert aus Cache ab (L1 -> L2 -> L3)."""

        # L1: Memory Cache
        if key in self.memory_cache:
            item = self.memory_cache[key]
            if time.time() < item['expires_at']:
                return item['value']
            else:
                del self.memory_cache[key]

        # L2: Redis Cache
        redis_value = await self.redis_client.get(f"cache:{key}")
        if redis_value:
            try:
                value = pickle.loads(redis_value)
                # Zurück in L1 Cache
                await self._set_memory_cache(key, value)
                return value
            except Exception:
                pass

        # L3: Database Cache
        db_value = await self._get_from_db_cache(key)
        if db_value:
            # Zurück in L2 und L1 Cache
            await self._set_redis_cache(key, db_value)
            await self._set_memory_cache(key, db_value)
            return db_value

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Setzt Wert in allen Cache-Leveln."""

        # L1: Memory Cache
        await self._set_memory_cache(key, value, ttl)

        # L2: Redis Cache
        await self._set_redis_cache(key, value, ttl)

        # L3: Database Cache
        await self._set_db_cache(key, value, ttl)

    async def _set_memory_cache(self, key: str, value: Any, ttl: Optional[int] = None):
        """Setzt Wert in Memory Cache."""

        # Memory-Cache-Größe begrenzen
        if len(self.memory_cache) >= self.memory_max_size:
            # LRU-Eviction (vereinfacht)
            oldest_key = min(
                self.memory_cache.keys(),
                key=lambda k: self.memory_cache[k]['created_at']
            )
            del self.memory_cache[oldest_key]

        expires_at = time.time() + (ttl or self.memory_ttl)
        self.memory_cache[key] = {
            'value': value,
            'created_at': time.time(),
            'expires_at': expires_at
        }

    async def _set_redis_cache(self, key: str, value: Any, ttl: Optional[int] = None):
        """Setzt Wert in Redis Cache."""

        try:
            serialized_value = pickle.dumps(value)
            await self.redis_client.setex(
                f"cache:{key}",
                ttl or self.redis_ttl,
                serialized_value
            )
        except Exception as e:
            print(f"Redis cache error: {e}")

    async def _set_db_cache(self, key: str, value: Any, ttl: Optional[int] = None):
        """Setzt Wert in Database Cache."""

        async with self.db_session_factory() as session:
            try:
                # Bestehenden Cache-Eintrag aktualisieren oder erstellen
                cache_entry = CacheEntryModel(
                    key=key,
                    value=json.dumps(value, default=str),
                    expires_at=datetime.utcnow() + timedelta(seconds=ttl or self.db_ttl)
                )

                await session.merge(cache_entry)
                await session.commit()

            except Exception as e:
                print(f"Database cache error: {e}")
                await session.rollback()

# Smart Caching Decorator
def smart_cache(
    ttl: int = 3600,
    key_prefix: str = "",
    cache_null: bool = False,
    serialize_args: bool = True
):
    """Smart Caching Decorator mit automatischer Key-Generierung."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Cache-Key generieren
            if serialize_args:
                key_data = {
                    'func': f"{func.__module__}.{func.__name__}",
                    'args': args,
                    'kwargs': kwargs
                }
                key_hash = hashlib.md5(
                    json.dumps(key_data, sort_keys=True, default=str).encode()
                ).hexdigest()
            else:
                key_hash = f"{func.__name__}_{hash((args, tuple(kwargs.items())))}"

            cache_key = f"{key_prefix}{key_hash}"

            # Cache prüfen
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Funktion ausführen
            result = await func(*args, **kwargs)

            # Ergebnis cachen (wenn nicht None oder cache_null=True)
            if result is not None or cache_null:
                await cache.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator

# Verwendung
@smart_cache(ttl=1800, key_prefix="agent_stats:")
async def get_agent_statistics(agent_id: str, date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
    """Ruft Agent-Statistiken ab (gecacht)."""

    # Teure Database-Query
    async with session_factory() as session:
        query = (
            select(
                func.count(TaskModel.id).label('total_tasks'),
                func.avg(TaskModel.duration).label('avg_duration'),
                func.sum(case((TaskModel.status == 'completed', 1), else_=0)).label('completed_tasks')
            )
            .where(
                TaskModel.agent_id == agent_id,
                TaskModel.created_at.between(date_range[0], date_range[1])
            )
        )

        result = await session.execute(query)
        row = result.first()

        return {
            'total_tasks': row.total_tasks or 0,
            'avg_duration': float(row.avg_duration or 0),
            'completed_tasks': row.completed_tasks or 0,
            'success_rate': (row.completed_tasks or 0) / max(row.total_tasks or 1, 1)
        }
```

## 🔧 Memory Optimization

### Memory-Efficient Data Processing

```python
import gc
from typing import Iterator, Generator
import psutil
import os

class MemoryOptimizedProcessor:
    """Memory-optimierter Daten-Processor."""

    def __init__(self, memory_limit_mb: int = 1024):
        self.memory_limit_bytes = memory_limit_mb * 1024 * 1024
        self.process = psutil.Process(os.getpid())

    def get_memory_usage(self) -> int:
        """Ruft aktuellen Speicherverbrauch ab."""
        return self.process.memory_info().rss

    def check_memory_limit(self) -> bool:
        """Prüft ob Speicherlimit erreicht ist."""
        return self.get_memory_usage() > self.memory_limit_bytes

    async def process_large_dataset(self, data_source: str, chunk_size: int = 1000) -> Iterator[Dict[str, Any]]:
        """Verarbeitet große Datasets in Chunks."""

        async for chunk in self._read_data_chunks(data_source, chunk_size):
            # Memory-Check vor Verarbeitung
            if self.check_memory_limit():
                gc.collect()  # Garbage Collection erzwingen

                if self.check_memory_limit():
                    raise MemoryError("Memory limit exceeded")

            # Chunk verarbeiten
            processed_chunk = await self._process_chunk(chunk)

            yield processed_chunk

            # Chunk aus Memory entfernen
            del chunk
            del processed_chunk

    async def _read_data_chunks(self, data_source: str, chunk_size: int) -> Generator[List[Dict[str, Any]], None, None]:
        """Liest Daten in Chunks."""

        if data_source.endswith('.csv'):
            import pandas as pd

            # Pandas Chunking für CSV
            for chunk_df in pd.read_csv(data_source, chunksize=chunk_size):
                yield chunk_df.to_dict('records')

        elif data_source.endswith('.json'):
            import ijson

            # Streaming JSON Parser
            with open(data_source, 'rb') as file:
                parser = ijson.items(file, 'item')

                chunk = []
                for item in parser:
                    chunk.append(item)

                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []

                if chunk:
                    yield chunk

    async def _process_chunk(self, chunk: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verarbeitet einzelnen Chunk."""

        # Memory-effiziente Verarbeitung
        result = {
            'processed_count': len(chunk),
            'memory_usage_mb': self.get_memory_usage() / 1024 / 1024
        }

        # Chunk-spezifische Verarbeitung
        for item in chunk:
            # Verarbeitung ohne große Zwischenspeicherung
            pass

        return result

# Memory-Pool für Object-Reuse
class ObjectPool:
    """Object-Pool für Memory-Optimierung."""

    def __init__(self, factory_func: Callable, max_size: int = 100):
        self.factory_func = factory_func
        self.max_size = max_size
        self.pool = []
        self.in_use = set()

    def acquire(self):
        """Holt Objekt aus Pool."""
        if self.pool:
            obj = self.pool.pop()
        else:
            obj = self.factory_func()

        self.in_use.add(id(obj))
        return obj

    def release(self, obj):
        """Gibt Objekt an Pool zurück."""
        obj_id = id(obj)

        if obj_id in self.in_use:
            self.in_use.remove(obj_id)

            # Objekt zurücksetzen
            if hasattr(obj, 'reset'):
                obj.reset()

            # Pool-Größe begrenzen
            if len(self.pool) < self.max_size:
                self.pool.append(obj)

# Task-Result-Pool für bessere Memory-Nutzung
task_result_pool = ObjectPool(
    factory_func=lambda: TaskResult(success=False, data=None),
    max_size=50
)

class MemoryOptimizedTaskExecutor:
    """Memory-optimierter Task-Executor."""

    async def execute_task(self, task: Task) -> TaskResult:
        """Führt Task memory-optimiert aus."""

        # TaskResult aus Pool holen
        result = task_result_pool.acquire()

        try:
            # Task ausführen
            execution_result = await self._perform_task_execution(task)

            # Result konfigurieren
            result.success = True
            result.data = execution_result
            result.execution_time = time.time() - task.start_time

            # Kopie für Rückgabe erstellen
            result_copy = TaskResult(
                success=result.success,
                data=result.data.copy() if isinstance(result.data, dict) else result.data,
                execution_time=result.execution_time
            )

            return result_copy

        finally:
            # Result an Pool zurückgeben
            task_result_pool.release(result)
```

!!! tip "Performance-Monitoring"
    Überwachen Sie kontinuierlich die Performance-Metriken und passen Sie die Optimierungen basierend auf realen Nutzungsmustern an.

!!! warning "Memory-Management"
    Bei großen Datasets ist sorgfältiges Memory-Management essentiell. Nutzen Sie Streaming, Chunking und Object-Pooling für optimale Speichernutzung.

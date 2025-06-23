from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.memories_view import MemoriesView
from backend import MemoryRecord


def test_set_memories_populates_view():
    view = MemoriesView()
    records = [
        MemoryRecord(key='1', kind='note', content='hello'),
        MemoryRecord(key='2', kind='pref', content='bye'),
    ]
    view.set_memories(records)
    assert len(view.memories.controls) == 2
    first = view.memories.controls[0]
    assert first.title.value == 'note'
    assert first.subtitle.value == 'hello'

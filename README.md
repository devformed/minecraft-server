# Devformed Fabric 26.2

Готовый воспроизводимый модпак для Minecraft 26.2, Fabric Loader 0.19.3 и Java 25.

В наборе 13 исходно запрошенных модов, 2 поддерживаемые замены и 7 обязательных зависимостей. JAR-файлы не хранятся в Git: готовый `.mrpack` скачивает их с официальных страниц релизов и проверяет SHA-512. Так ветка остаётся небольшой и не нарушает ограничения модов с закрытой лицензией.

## Быстрый запуск клиента

1. Скачай [`release/devformed-fabric-26.2.mrpack`](release/devformed-fabric-26.2.mrpack).
2. В Prism Launcher выбери **Add Instance → Import** и укажи этот файл.
3. Убедись, что для инстанса выбрана Java 25. Minecraft и Fabric Loader Prism установит из зафиксированного manifest.

Если pack собирается из checkout заново:

```bash
python3 tools/modpack.py build
python3 tools/modpack.py verify
```

## Что вошло

| Мод | Версия | Сторона | Статус |
|---|---|---|---|
| Goblin Traders | 1.12.0 | client + server | официальный Fabric-релиз |
| Reconnectible Chains | 1.2.6 | client + server | замена архивированного Connectible Chains |
| Eating Animation Fork | 2.1.0 | client | замена оригинального Eating Animation |
| Falling Leaves | 2.0.7 | client | официальный релиз помечен совместимым с 26.2 |
| Just Enough Items | 30.15.0.121 | client | beta |
| Mouse Tweaks | 2.31 | client | официальный релиз |
| Explorer's Compass | 2.5.1 | client + server | официальный релиз |
| Connected Glass | 1.1.14 | client + server | официальный релиз |
| LambDynamicLights | 4.12.2 | client | официальный релиз |
| Catalogue | 1.12.3 | client | официальный релиз |
| Dark Paintings | 26.2.0.1 | client + server | официальный релиз |
| Variants&Ventures | 1.0.26 | client + server | официальный релиз |
| I'm Fast | 1.0.3 | server | не устанавливается в клиентский инстанс |
| Freecam | 1.4.1-beta.3 | client | beta |
| Better Than Mending | 2.3.0 | client + server | официальный merged Fabric/NeoForge JAR |

Обязательные зависимости также зафиксированы: Fabric API, Cloth Config, Fusion, SuperMartijn642's Core Lib, YACL, Resourceful Lib и Framework. Fabric Language Kotlin, Balm, Bookshelf, Architectury и Puzzles Lib этому набору не нужны.

## Получить обычную папку `mods`

Утилита скачивает только официальные immutable-файлы, проверяет размер, SHA-1, SHA-512, целостность ZIP и `fabric.mod.json`.

```bash
# Клиент: 21 JAR (14 модов/замен + 7 зависимостей)
python3 tools/modpack.py materialize client build/client/mods

# Сервер: 14 JAR, включая server-only I'm Fast
python3 tools/modpack.py materialize server build/server/mods
```

`build/` намеренно не попадает в Git. Полный источник истины — [`pack/mods.lock.json`](pack/mods.lock.json); стандартный Modrinth manifest — [`pack/modrinth.index.json`](pack/modrinth.index.json).

## Что не вошло

Для Enderman Overhaul, From The Fog, Blossom Blade, Naturalist и Ribbits нет официального Fabric-релиза, явно совместимого с Minecraft 26.2. AI Improvements для 26.2 выпущен только под NeoForge. Старые несовместимые JAR не подмешиваются. Подробности и ссылки находятся в [`pack/unsupported.json`](pack/unsupported.json).

Источники и лицензии перечислены в [`pack/NOTICE.md`](pack/NOTICE.md).

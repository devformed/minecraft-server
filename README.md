# Devformed Fabric 26.2

Воспроизводимый модпак для **Minecraft 26.2**, **Fabric Loader 0.19.3** и **Java 25**.

В составе 25 пользовательских модов: 23 прямых выбора и 2 поддерживаемые замены. Ещё 7 технических зависимостей подтягиваются автоматически. Получается **32 JAR на клиенте** и **19 JAR на сервере**. JAR-файлы не хранятся в Git: сборщик скачивает зафиксированные официальные релизы и проверяет их хеши.

## Быстрый запуск клиента

### Официальный Minecraft Launcher

1. Установи профиль **Fabric Loader 0.19.3** для **Minecraft 26.2** через [Fabric Installer 1.1.2](https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.1.2/fabric-installer-1.1.2.jar).
2. Выбери для профиля **Java 25**.
3. Подготовь изолированную игровую директорию с модами и конфигами:

```bash
python3 tools/modpack.py materialize-instance client build/client --clean
```

4. Укажи `build/client` как game directory профиля либо перенеси её содержимое в отдельную директорию профиля.

### Prism Launcher

1. Скачай [`release/devformed-fabric-26.2.mrpack`](release/devformed-fabric-26.2.mrpack).
2. Выбери **Add Instance → Import** и укажи файл.
3. Назначь инстансу **Java 25**. Minecraft и Fabric Loader установятся из зафиксированного manifest.

## Оптимизация — по убыванию важности

<a href="https://modrinth.com/mod/bobby"><img src="https://cdn.modrinth.com/data/M08ruV16/icon.png" alt="Bobby" width="48" height="48" align="left"></a>
**[Bobby](https://modrinth.com/mod/bobby)** · `5.2.15+mc26.2` · `client`<br>
Кеширует дальние серверные чанки.
<br clear="left">

<a href="https://modrinth.com/mod/sodium"><img src="https://cdn.modrinth.com/data/AANobbMI/295862f4724dc3f78df3447ad6072b2dcd3ef0c9_96.webp" alt="Sodium" width="48" height="48" align="left"></a>
**[Sodium](https://modrinth.com/mod/sodium)** · `0.9.1` · `client`<br>
Быстрее рендерит мир.
<br clear="left">

<a href="https://modrinth.com/mod/c2me-fabric"><img src="https://cdn.modrinth.com/data/VSNURh3q/3c2ce471054466712a44c8758a03e03bb868f93b_96.webp" alt="C2ME" width="48" height="48" align="left"></a>
**[C2ME](https://modrinth.com/mod/c2me-fabric)** · `0.4.1-beta.1.0` · `client + server` · `beta`<br>
Распараллеливает загрузку чанков.
<br clear="left">

<a href="https://modrinth.com/mod/lithium"><img src="https://cdn.modrinth.com/data/gvQqBUqZ/bcc8686c13af0143adf4285d741256af824f70b7_96.webp" alt="Lithium" width="48" height="48" align="left"></a>
**[Lithium](https://modrinth.com/mod/lithium)** · `0.25.3` · `client + server`<br>
Ускоряет игровую логику.
<br clear="left">

<a href="https://modrinth.com/mod/zfastnoise"><img src="https://cdn.modrinth.com/data/OnlVIpq5/6f2393cd87c37ef685efb82aacc5b0c9fae0c28d.png" alt="Fast Noise" width="48" height="48" align="left"></a>
**[Fast Noise](https://modrinth.com/mod/zfastnoise)** · `1.0.39` · `client + server`<br>
Ускоряет шум worldgen.
<br clear="left">

<a href="https://modrinth.com/mod/scalablelux"><img src="https://cdn.modrinth.com/data/Ps1zyz6x/27133942a1a58af1bb11b087957ea4cc14414dd3_96.webp" alt="ScalableLux" width="48" height="48" align="left"></a>
**[ScalableLux](https://modrinth.com/mod/scalablelux)** · `0.2.1` · `client + server`<br>
Параллельно пересчитывает свет.
<br clear="left">

<a href="https://modrinth.com/mod/ferrite-core"><img src="https://cdn.modrinth.com/data/uXXizFIs/222a126f26f8f9ae1eb339f3b767677f18bff31f_96.webp" alt="FerriteCore" width="48" height="48" align="left"></a>
**[FerriteCore](https://modrinth.com/mod/ferrite-core)** · `9.0.0` · `client + server`<br>
Снижает расход памяти.
<br clear="left">

<a href="https://modrinth.com/mod/immediatelyfast"><img src="https://cdn.modrinth.com/data/5ZwdcRci/e57b6b451425692ac17ad322d5e14bea686a383a_96.webp" alt="ImmediatelyFast" width="48" height="48" align="left"></a>
**[ImmediatelyFast](https://modrinth.com/mod/immediatelyfast)** · `1.16.2` · `client`<br>
Батчит отрисовку GUI и частиц.
<br clear="left">

<a href="https://modrinth.com/mod/entityculling"><img src="https://cdn.modrinth.com/data/NNAgCjsB/7873452d6cede4daed12da3d7d8c193ab88b4fd6_96.webp" alt="Entity Culling" width="48" height="48" align="left"></a>
**[Entity Culling](https://modrinth.com/mod/entityculling)** · `1.10.5` · `client`<br>
Не рисует скрытые сущности.
<br clear="left">

<a href="https://modrinth.com/mod/moreculling"><img src="https://cdn.modrinth.com/data/51shyZVL/c51b07193b56e952269ef50101d12aecba2b4747_96.webp" alt="More Culling" width="48" height="48" align="left"></a>
**[More Culling](https://modrinth.com/mod/moreculling)** · `1.8.0` · `client`<br>
Не рисует скрытые грани.
<br clear="left">

<a href="https://modrinth.com/plugin/chunky"><img src="https://cdn.modrinth.com/data/fALzjamp/e1954413665e57b7bae1feef44eda530270c7d47_96.webp" alt="Chunky" width="48" height="48" align="left"></a>
**[Chunky](https://modrinth.com/plugin/chunky)** · `1.5.3` · `client + server`<br>
Предгенерирует чанки командой.
<br clear="left">

Sodium Extra, Reese's Sodium Options, Iris и ModernFix намеренно не включены: это необязательные настройки, шейдеры и более агрессивные вмешательства поверх базового стека.

## Контент и удобство — по убыванию важности

<a href="https://modrinth.com/mod/jei"><img src="https://cdn.modrinth.com/data/u6dRKJwZ/4a3f18ac0d096c9f8e9176984c44be4e58f94c89_96.webp" alt="Just Enough Items" width="48" height="48" align="left"></a>
**[Just Enough Items (JEI)](https://modrinth.com/mod/jei)** · `30.15.0.121` · `client` · `beta`<br>
Рецепты и применение предметов.
<br clear="left">

<a href="https://modrinth.com/mod/explorers-compass"><img src="https://cdn.modrinth.com/data/RV1qfVQ8/8f36254e98a4caa95684fcf4dbe72c2264c98cfc.png" alt="Explorer's Compass" width="48" height="48" align="left"></a>
**[Explorer's Compass](https://modrinth.com/mod/explorers-compass)** · `2.5.1` · `client + server`<br>
Поиск структур компасом.
<br clear="left">

<a href="https://modrinth.com/mod/mouse-tweaks"><img src="https://cdn.modrinth.com/data/aC3cM3Vq/6c0eaa4e60a9c87f4766f222ff63286f09da32c0_96.webp" alt="Mouse Tweaks" width="48" height="48" align="left"></a>
**[Mouse Tweaks](https://modrinth.com/mod/mouse-tweaks)** · `2.31` · `client`<br>
Быстрые жесты в инвентаре.
<br clear="left">

<a href="https://modrinth.com/mod/better-than-mending"><img src="https://cdn.modrinth.com/data/Lvv4SHrK/icon.png" alt="Better Than Mending" width="48" height="48" align="left"></a>
**[Better Than Mending](https://modrinth.com/mod/better-than-mending)** · `2.3.0` · `client + server`<br>
Ручной ремонт предметов опытом.
<br clear="left">

<a href="https://github.com/MrCrayfish/GoblinTraders"><img src="docs/images/mods/goblin-traders.png" alt="Goblin Traders" width="48" height="48" align="left"></a>
**[Goblin Traders](https://github.com/MrCrayfish/GoblinTraders)** · `1.12.0` · `client + server`<br>
Гоблины с редкими сделками.
<br clear="left">

<a href="https://modrinth.com/mod/variants-and-ventures"><img src="https://cdn.modrinth.com/data/lNDRiXkY/bd6e91737946cf99c155c94108e98df8248e3078_96.webp" alt="Variants and Ventures" width="48" height="48" align="left"></a>
**[Variants&Ventures](https://modrinth.com/mod/variants-and-ventures)** · `1.0.26` · `client + server`<br>
Новые варианты знакомых мобов.
<br clear="left">

<a href="https://modrinth.com/mod/connected-glass"><img src="https://cdn.modrinth.com/data/DghO0R02/icon.png" alt="Connected Glass" width="48" height="48" align="left"></a>
**[Connected Glass](https://modrinth.com/mod/connected-glass)** · `1.1.14` · `client + server`<br>
Стекло без внутренних швов.
<br clear="left">

<a href="https://modrinth.com/mod/lambdynamiclights"><img src="https://cdn.modrinth.com/data/yBW8D80W/d4f5c3ff8df7caf024178b04eca6d69f95979cfe_96.webp" alt="LambDynamicLights" width="48" height="48" align="left"></a>
**[LambDynamicLights](https://modrinth.com/mod/lambdynamiclights)** · `4.12.2` · `client`<br>
Динамический свет от предметов.
<br clear="left">

<a href="https://modrinth.com/mod/reconnectible-chains"><img src="https://cdn.modrinth.com/data/5pzBXDS3/4b39899334d0cc0a7270ae178da42e6aa9444c6a_96.webp" alt="Reconnectible Chains" width="48" height="48" align="left"></a>
**[Reconnectible Chains](https://modrinth.com/mod/reconnectible-chains)** · `1.2.6` · `client + server` · замена Connectible Chains<br>
Декоративные цепи между заборами.
<br clear="left">

<a href="https://modrinth.com/mod/freecam"><img src="https://cdn.modrinth.com/data/XeEZ3fK2/9529a900a2aa6ed56c1b3167f165bac91b3acd6e_96.webp" alt="Freecam" width="48" height="48" align="left"></a>
**[Freecam](https://modrinth.com/mod/freecam)** · `1.4.1-beta.3` · `client` · `beta`<br>
Свободная камера без движения игрока.
<br clear="left">

<a href="https://github.com/MrCrayfish/Catalogue"><img src="docs/images/mods/catalogue.png" alt="Catalogue" width="48" height="48" align="left"></a>
**[Catalogue](https://github.com/MrCrayfish/Catalogue)** · `1.12.3` · `client`<br>
Экран списка и настроек модов.
<br clear="left">

<a href="https://modrinth.com/mod/dark-paintings"><img src="https://cdn.modrinth.com/data/lFGQ4Hnk/1dd928b82ae0f65ca0d864af148f7d44875340c6.png" alt="Dark Paintings" width="48" height="48" align="left"></a>
**[Dark Paintings](https://modrinth.com/mod/dark-paintings)** · `26.2.0.1` · `client + server`<br>
Множество новых картин.
<br clear="left">

<a href="https://modrinth.com/mod/fallingleaves"><img src="https://cdn.modrinth.com/data/WhbRG4iK/58f5b66cb54787d9c25228d667f61144371c3867_96.webp" alt="Falling Leaves" width="48" height="48" align="left"></a>
**[Falling Leaves](https://modrinth.com/mod/fallingleaves)** · `2.0.7` · `client`<br>
Падающие листья под деревьями.
<br clear="left">

<a href="https://modrinth.com/mod/eating-animation-fork"><img src="docs/images/mods/eating-animation-fork.png" alt="Eating Animation Fork" width="48" height="48" align="left"></a>
**[Eating Animation Fork](https://modrinth.com/mod/eating-animation-fork)** · `2.1.0` · `client` · замена Eating Animation<br>
Еда видна во время еды.
<br clear="left">

<details>
<summary><strong>7 технических зависимостей</strong></summary>

- Fabric API
- Cloth Config
- Fusion
- SuperMartijn642's Core Lib
- YetAnotherConfigLib (YACL)
- Resourceful Lib
- Framework

</details>

## Сервер и проверка сборки

```bash
# Подготовить клиент: 32 JAR и pack overrides.
python3 tools/modpack.py materialize-instance client build/client --clean

# Подготовить сервер: только 19 совместимых JAR.
python3 tools/modpack.py materialize server build/server/mods --clean

# Пересобрать manifest и .mrpack, затем проверить lock/index/archive.
python3 tools/modpack.py build
python3 tools/modpack.py verify
```

`materialize` скачивает и проверяет JAR только для выбранной стороны; `materialize-instance` дополнительно применяет `pack/overrides` к готовой игровой директории. `build/` намеренно не попадает в Git. Полный источник истины — [`pack/mods.lock.json`](pack/mods.lock.json); стандартный Modrinth manifest — [`pack/modrinth.index.json`](pack/modrinth.index.json).

Готовый сервер запускается через Docker Compose на Java 25. Sidecar делает согласованные Restic-снимки: каждый снимок логически полный, но неизменившиеся блоки физически не копируются. Команды запуска, ручного бэкапа, проверки и восстановления находятся в [`server/README.md`](server/README.md).

## Что не вошло

Для Enderman Overhaul, From The Fog, Blossom Blade, Naturalist и Ribbits нет официального Fabric-релиза, явно совместимого с Minecraft 26.2. AI Improvements для 26.2 выпущен только под NeoForge. I'm Fast исключён: это не оптимизация, а отключение серверных проверок движения. Несовместимые JAR не подмешиваются; подробности находятся в [`pack/unsupported.json`](pack/unsupported.json).

Источники и лицензии перечислены в [`pack/NOTICE.md`](pack/NOTICE.md).
